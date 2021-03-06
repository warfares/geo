from bottle import *
from geo.model import *
import geo.rest.vo as vo
import json

@post('group/staticbbox')
def staticbbox():
	o = json.load(request.body)
	vo_layers = o['layers']
	layers = map(lambda l: Layer(l['name']), vo_layers)
	group = Group(layers)
	bbox = group.static_bbox()
	return vo.bbox(bbox)

@post('group/withinpoint')
def withinpoint():
	o = json.load(request.body)
	vo_layers = o['layers']
	fields = o['fields']
	x = o['point']['x']
	y = o['point']['y']
	dist = o['dist']

	layers = map(lambda l: Layer(l['name'],l['srid']), vo_layers)
	group = Group(layers)
	point = Point(x,y)
	geoms = group.within_point(fields,point, dist)
	
	out = map(lambda g: vo.geometry(g), geoms)
	return vo.collection(out, len(out))

@post('group/withinbbox')
def withinbbox():
	o = json.load(request.body)
	vo_layers = o['layers']
	vo_bbox = o['bbox']
	
	point_min = Point(vo_bbox['xmin'],vo_bbox['ymin'])
	point_max = Point(vo_bbox['xmax'],vo_bbox['ymax'])
	
	bbox = Bbox(point_min, point_max)
	layers = map(lambda l: Layer(l['name'],l['srid']), vo_layers)
	group = Group(layers)
	
	layers_out = group.within_bbox(bbox)
	
	out = map(lambda l: vo.layer(l), layers_out)
	return vo.collection(out, len(out))