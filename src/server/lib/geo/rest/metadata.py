from bottle import *
from geo.model import *
import geo.rest.vo as vo

@route('/metadata/distinct_values')
def distinct_values():
	name = request.GET.get('name')
	layer_name = request.GET.get('layer')
	limit = request.GET.get('limit')
	m = Metadata(name)
	values = m.distinct_values(layer_name, limit)
	return vo.collection(values, len(values))