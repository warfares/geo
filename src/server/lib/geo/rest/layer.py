from bottle import *
from geo.model import *
import geo.rest.vo as vo
import json

@route('/layer/:layer_name/metadata')
def metadata(layer_name):
	l = Layer(layer_name,0)
	metadatas = map(lambda m: vo.metadata(m), l.metadata())
	return vo.collection(metadatas, len(metadatas))
	
@post('layer/query')
def query():
	o = json.load(request.body)
	layer_name = o['layer']
	fields = o['fields']
	criteria = o['criteria']
	
	l = Layer(layer_name,0)
	result = l.query(fields, criteria)
	
	return {'result': result }

@route('/layer/:layer_name/bbox')
def bbox(layer_name):
	l = Layer(layer_name,32719)
	bbox = l.bbox(96)
	return vo.bbox(bbox)

@route('/layer/:layer_name/staticbbox')
def static_bbox(layer_name):
	l = Layer(layer_name,0)
	bbox = l.static_bbox()
	return vo.bbox(bbox)