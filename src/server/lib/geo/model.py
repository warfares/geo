#!/usr/bin/env python
# encoding: utf-8
"""
geo.py

Created by Rodolfo  Barriga.
"""

from psycopg2 import connect
import psycopg2.extras
import sys

CONN_STR = 'user=postgres password=postgres dbname=pelambre'
#TODO check data connection level..


class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def wkt(self):
		return 'POINT(%s %s)' %(self.x, self.y)

class Bbox:
	def __init__(self, point_min, point_max):
		self.point_min = point_min
		self.point_max = point_max

	def wkt(self):
		top_left = '%s %s' %(self.point_min.x, self.point_max.y)
		top_right = '%s %s' %(self.point_max.x, self.point_max.y)
		bottom_left = '%s %s' %(self.point_min.x, self.point_min.y)
		bottom_right = '%s %s' %(self.point_max.x, self.point_min.y)
		return  'POLYGON((%s, %s, %s, %s, %s))'  %(bottom_left, bottom_right, top_right, top_left, bottom_left);
		
class Metadata:
	def __init__(self, name, type):
		self.name = name
		self.type = type

class Layer:
	def __init__(self, name, srid):
		self.name = name
		self.srid = srid
	
	def metadata(self):
		conn = connect(CONN_STR)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		r = self.name.split('.')
		schema = ''
		name = ''
		if (len(r)>1):
			schema = r[0]
			name = r[1] 

		sql = 'select column_name, data_type '
		sql += 'from information_schema.columns '
		sql += 'where table_schema = \'%s\' ' % schema
		sql += 'and  table_name = \'%s\' ' % name
		sql += 'and column_name != \'%s\';' % 'the_geom'

		cursor.execute(sql)
		rows = cursor.fetchall()

		metadatas = []
		for row in rows:
			m = Metadata(row['column_name'], row['data_type'])
			metadatas.append(m)
			
		cursor.close()
		conn.close()
		return metadatas
	
	#TODO limit 
	#TODO criteria building
	def query(self, fields, criteria):
		
		conn = connect(CONN_STR)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		sql = 'select %s ' % fields
		sql += 'from %s ' % self.name
		
		cursor.execute(sql)
		rows = cursor.fetchall()

		results = []
		result = {}
		
		#building dynamic output dictionary from the fields
		for row in rows:
			for f in fields.split(','):
				result[f] = row[f]
			
			results.append(result)

		cursor.close()
		conn.close()
		return results
		
		
	def bbox(self, to_srid):
		conn = connect(CONN_STR)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		
		sql = 'select '
		sql += 'st_xmin(transform(st_setSRID(r.box, %s), %s)) as xmin, ' % (self.srid, to_srid)
		sql += 'st_ymin(transform(st_setSRID(r.box, %s), %s)) as ymin, ' % (self.srid, to_srid)
		sql += 'st_xmax(transform(st_setSRID(r.box, %s), %s)) as xmax, ' % (self.srid, to_srid)
		sql += 'st_ymax(transform(st_setSRID(r.box, %s), %s)) as ymax ' % (self.srid, to_srid)
		sql += 'from (select st_extent(the_geom) as box from %s) as r ' % (self.name)

		cursor.execute(sql)
		row = cursor.fetchone()
		
		bbox = Bbox(Point(row['xmin'], row['ymin']), Point(row['xmax'], row['ymax']))
		
		cursor.close()
		conn.close()
		
		return bbox
	
	def static_bbox(self):
		conn = connect(CONN_STR)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		
		sql = 'select "left", bottom, "right", top from geometry_columns '
		sql += 'where f_table_name = \'%s\'' % (self.name.split('.')[1])

		cursor.execute(sql)
		row = cursor.fetchone()
		
		bbox = Bbox(Point(row['left'], row['bottom']), Point(row['right'], row['top']))
		
		cursor.close()
		conn.close()
		return bbox
	
	#OK
	def closest_point(self, point):
		conn = connect(CONN_STR)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		
		geometry = 'st_geomfromtext( \'%s\', %s )' % (point.wkt(), self.srid)

		sql = 'select '
		sql += 'st_x(the_geom) as x, '
		sql += 'st_y(the_geom) as y, '
		sql += 'st_distance( %s, the_geom) as dist ' % geometry
		sql += 'from %s ' % self.name
		sql += 'order by dist '
		sql += 'limit 1'

		cursor.execute(sql)
		row = cursor.fetchone()

		p = Point(row['x'], row['y'])

		cursor.close()
		conn.close()
		
		return p

class Geometry:
	def __init__(self,id,layer):
		self.id = id
		self.layer = layer

class Group:
	def __init__(self, layers):
		self.layers = layers
		
	
	def static_bbox(self):
		conn = connect(CONN_STR)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
		sql = ''
		for layer in self.layers:
			if len(sql) > 0:
				sql += ' union all '
				
			sql += 'select "left", bottom, "right", top from geometry_columns '
			sql += 'where f_table_name = \'%s\' ' % (layer.name.split('.')[1])
	
		cursor.execute(sql)
		rows = cursor.fetchall()
		
		left = []
		bottom = []
		right = []
		top = []

		for row in rows:
			left.append(row['left'])
			bottom.append(row['bottom'])
			right.append(row['right'])
			top.append(row['top'])
			
		bbox = Bbox(Point(min(left), min(bottom)), Point(max(right), max(top)))
		
		return bbox
		
	def within_point(self,fields,point,dist):
		conn = connect(CONN_STR)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		
		sql = ''
		for layer in self.layers:
			geom = 'st_geomfromtext( \'%s\', %s )' % (point.wkt(), '96')
			transGeom = 'transform(%s,%s)' % (geom, layer.srid)

			if len(sql) > 0:
				sql += ' union all '

			sql += 'select character varying \'%s\' as layer_name, ' % layer.name
			sql += 'st_distance( %s, the_geom) as dist, ' % transGeom
			sql += 'gid, '
			sql += '%s ' % fields
			sql += 'from %s where ' % layer.name
			sql += 'st_dwithin(the_geom, %s, %s) ' % (transGeom, dist)

		cursor.execute(sql)
		rows = cursor.fetchall()
				
		geoms = []
		for row in rows:
			g = Geometry(row['gid'], Layer(row['layer_name'], 0))
			geoms.append(g)
		
		cursor.close()
		conn.close()
		return geoms

	def within_bbox(self, bbox):
		conn = connect(CONN_STR)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		
		sql = ''
		for layer in self.layers:
			geom = 'st_geomfromtext( \'%s\', %s )' % (bbox.wkt(), '96')
			transGeom = 'transform(%s,%s)' % (geom, layer.srid)
	
			if len(sql) > 0:
				sql += ' union all '
			
			sql += '(select character varying \'%s\' as layer_name ' % layer.name
			sql += 'from %s where ' % layer.name
			sql += 'st_dwithin(the_geom, %s, %s) ' % (transGeom, 0)
			sql += 'limit 1 )'

		cursor.execute(sql)
		rows = cursor.fetchall()
		
		layers = []
		for row in rows:
			l = Layer(row['layer_name'], 0)
			layers.append(l)
		
		cursor.close()
		conn.close()
		return layers

	#TODO
	def closest_point(self, point):
		points = []
		for layer in self.layers:
			p = layer.closest_point(point)
			points.append(p)
		#TODO min by distance
		return points