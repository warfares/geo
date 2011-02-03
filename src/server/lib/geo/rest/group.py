from bottle import *
from geo.model import *
from geo.rest.util import *
import geo.rest.vo as vo
import json

#OK 
@post('group/staticbbox')
def staticbbox():
	o = json.load(request.body)
	vo_layers = o['layers']
	layers = map(lambda l: Layer(l['name'],0), vo_layers)
	group = Group(layers)
	bbox = group.static_bbox()
	return vo.bbox(bbox)

#OK
@post('group/withinpoint')
def withinpoint():
	o = json.load(request.body)
	vo_layers = o['layers']
	fields = o['fields']
	x = o['point']['x']
	y = o['point']['y']
	dist = o['dist']

	layers = map(lambda l: Layer(l['name'],'24879'), vo_layers)
	group = Group(layers)
	point = Point(x,y)
	geoms = group.within_point(fields,point, dist)
	
	out = map(lambda g: vo.geometry(g), geoms)
	return {'geoms': out }

#OK
@post('group/withinbbox')
def withinbbox():
	o = json.load(request.body)
	vo_layers = o['layers']
	vo_bbox = o['bbox']
	
	point_min = Point(vo_bbox['minx'],vo_bbox['miny'])
	point_max = Point(vo_bbox['maxx'],vo_bbox['maxy'])
	
	bbox = Bbox(point_min, point_max)
	layers = map(lambda l: Layer(l['name'],'24879'), vo_layers)
	group = Group(layers)
	
	layers_out = group.within_bbox(bbox)
	
	out = map(lambda l: vo.layer(l), layers_out)
	return {'layers': out }

@route('/group/closestpoint')
def closestpoint():
	p = request.params
	layer_names = p['layerNames']
	srid = p['srid']
	x = p['x']
	y = p['y']
	group = Group(str_to_layers(layer_names, srid))
	points = group.closest_point(Point(x,y))
	
	vo = [];
	for p in points:
		vo.append({'x':p.x, 'y':p.y})
	return {'points': vo }