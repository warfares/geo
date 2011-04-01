from bottle import *
from geo.model import *
import geo.rest.vo as vo
import json

@get('/layer/metadata')
def metadata():
	layer_name = request.GET.get('layerName')	
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
	wkt = o['wkt']
	
	l = Layer(layer_name)
	results = l.query(fields, criteria, paging, start, limit,True, wkt)
	return vo.collection(results, l.query_count(criteria))


@get('/layer/bbox')
def bbox():
	layer_name = request.GET.get('layerName')
	srid = request.GET.get('srid')
	l = Layer(layer_name,32719)
	bbox = l.bbox(96)
	return vo.bbox(bbox)

@get('/layer/staticbbox')
def staticbbox():
	layer_name = request.GET.get('layerName')
	l = Layer(layer_name)
	bbox = l.static_bbox()
	return vo.bbox(bbox)