#!/usr/bin/env python
# encoding: utf-8
"""
geo.py

Created by Rodolfo  Barriga.
"""

import sys
import decimal
import geo.util as util

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
	def __init__(self, name, type=''):
		self.name = name
		self.type = type
	
	def distinct_values(self, layer_name, limit):
		
		sql = 'select distinct %s as values ' % self.name 
		sql += 'from %s where %s is not null ' % (layer_name, self.name)
		sql += 'limit %s' % limit
		
		dh = util.DataHelper()
		rows = dh.fetchall(sql)
		
		values = []
		for row in rows:
			v = row['values']
			if isinstance(v, decimal.Decimal): v = float(v)
			values.append({'values':v})

		dh.close()
		return values
		
class Layer:
	def __init__(self, name, srid=0):
		self.name = name
		self.srid = srid

	def metadata(self):

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
		sql += 'and column_name != \'%s\' ' % 'the_geom'
		sql += 'order by ordinal_position;'

		dh = util.DataHelper()
		rows = dh.fetchall(sql)

		metadatas = []
		for row in rows:
			m = Metadata(row['column_name'], row['data_type'])
			metadatas.append(m)
			
		dh.close()
		return metadatas
	
	def query_count(self, criteria):

		sql = 'select count(*) as count '
		sql += 'from %s ' % self.name

		if(criteria):
			sql += 'where %s ' % self.__criteria_to_sql(criteria)
		
		sql += ';'
		
		dh = util.DataHelper()
		row = dh.fetchone(sql)

		count = row['count']
		
		dh.close()
		return count
	
	def query(self, fields, criteria, paging=False, start=0, limit=0, order=False, wkt=False):
		
		#fields 
		sql = 'select %s ' % fields
		if(wkt):
			sql += ', astext(transform(the_geom, 96)) as wkt '
	
		#table
		sql += 'from %s ' % self.name
	
		#options 
		if(criteria):
			sql += 'where %s ' % self.__criteria_to_sql(criteria)
		
		if(order):
			sql += ' order by %s ' %(fields)
		
		if(paging):
			sql += ' offset %s limit %s ' %(start, limit)
		
		sql += ';'

		dh = util.DataHelper()
		rows = dh.fetchall(sql)

		results = []
		
		#building dynamic output dictionary from the fields
		for row in rows:
			result = {}
			for f in fields.split(','):
				v = row[f]
				if isinstance(v, decimal.Decimal): v = float(v)
				result[f] = v
			if('wkt' in row):
				result['wkt'] = row['wkt']
			
			results.append(result)

		dh.close()
		return results

	def __criteria_to_sql(self, criteria):
		sql = ''
		for c in criteria:
			row_id = c['rowID']
			and_or = c['andOr']
			column_name = c['columnName']
			operator_template = c['operatorTemplate']
			entry_values = c['entryValues']
			
			for i, v in enumerate(entry_values):
				operator_template = operator_template.replace('{' + str(i) + '}', str(v))
			
			sql += and_or + ' ' + column_name + ' ' + operator_template + ' '
			
		return sql

	def bbox(self, to_srid):
		
		sql = 'select '
		sql += 'st_xmin(transform(st_setSRID(r.box, %s), %s)) as xmin, ' % (self.srid, to_srid)
		sql += 'st_ymin(transform(st_setSRID(r.box, %s), %s)) as ymin, ' % (self.srid, to_srid)
		sql += 'st_xmax(transform(st_setSRID(r.box, %s), %s)) as xmax, ' % (self.srid, to_srid)
		sql += 'st_ymax(transform(st_setSRID(r.box, %s), %s)) as ymax ' % (self.srid, to_srid)
		sql += 'from (select st_extent(the_geom) as box from %s) as r ' % (self.name)

		dh = util.DataHelper()
		row = dh.fetchone(sql)
		
		bbox = Bbox(Point(row['xmin'], row['ymin']), Point(row['xmax'], row['ymax']))
		
		dh.close()
		return bbox
	
	def static_bbox(self):
		
		sql = 'select "left", bottom, "right", top from geometry_columns '
		sql += 'where f_table_name = \'%s\'' % (self.name.split('.')[1])

		dh = util.DataHelper()
		row = dh.fetchone(sql)
		
		bbox = Bbox(Point(row['left'], row['bottom']), Point(row['right'], row['top']))
		
		dh.close()
		return bbox
	
	def closest_point(self, point):
		
		geometry = 'st_geomfromtext( \'%s\', %s )' % (point.wkt(), self.srid)

		sql = 'select '
		sql += 'st_x(the_geom) as x, '
		sql += 'st_y(the_geom) as y, '
		sql += 'st_distance( %s, the_geom) as dist ' % geometry
		sql += 'from %s ' % self.name
		sql += 'order by dist '
		sql += 'limit 1'

		dh = util.DataHelper()
		row = dh.fetchone(sql)

		p = Point(row['x'], row['y'])

		dh.close()
		return p

class Geometry:
	def __init__(self,id,layer):
		self.id = id
		self.layer = layer

class Group:
	def __init__(self, layers):
		self.layers = layers
	
	def static_bbox(self):
		
		sql = ''
		for layer in self.layers:
			if len(sql) > 0:
				sql += ' union all '
				
			sql += 'select "left", bottom, "right", top from geometry_columns '
			sql += 'where f_table_name = \'%s\' ' % (layer.name.split('.')[1])
	
		dh = util.DataHelper()
		row = dh.fetchone(sql)
		
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
		
		dh.Close()
		return bbox
		
	def within_point(self,fields,point,dist):
		
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

		dh = util.DataHelper()
		rows = dh.fetchall(sql)
				
		geoms = []
		for row in rows:
			g = Geometry(row['gid'], Layer(row['layer_name'], 0))
			geoms.append(g)
		
		dh.close()
		return geoms

	def within_bbox(self, bbox):
		
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

		dh = util.DataHelper()
		rows = dh.fetchall(sql)
		
		layers = []
		for row in rows:
			l = Layer(row['layer_name'], 0)
			layers.append(l)
		
		dh.close()
		return layers

	#TODO
	def closest_point(self, point):
		
		points = []
		for layer in self.layers:
			p = layer.closest_point(point)
			points.append(p)
		#TODO min by distance
		return points