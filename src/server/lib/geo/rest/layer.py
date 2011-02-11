from bottle import *
from geo.model import *
import geo.rest.vo as vo
import json

@route('/layer/:layer_name/metadata')
def metadata(layer_name):
	l = Layer(layer_name)
	metadatas = map(lambda m: vo.metadata(m), l.metadata())
	return vo.collection(metadatas, len(metadatas))
	
@post('layer/query')
def query():
	o = json.load(request.body)
	layer_name = o['layer']
	fields = o['fields']
	criteria = o['criteria']
	paging = o['paging']
	start = o['start']
	limit = o['limit']
	
	l = Layer(layer_name)
	results = l.query(fields, criteria, paging, start, limit, True)
	return vo.collection(results, l.query_count(criteria))

#TODO Fix this static values 
@route('/layer/:layer_name/bbox')
def bbox(layer_name):
	l = Layer(layer_name,32719)
	bbox = l.bbox(96)
	return vo.bbox(bbox)

@route('/layer/:layer_name/staticbbox')
def static_bbox(layer_name):
	l = Layer(layer_name)
	bbox = l.static_bbox()
	return vo.bbox(bbox)