# vo-> objects python to JS notation 

#general purpose 
def collection(entities,total):
	vo = {
		'entities': entities,
		'total' : total
	}
	return vo

def metadata(o):
	vo = {
		'name':o.name,
		'type':o.type
	}
	return vo

def bbox(o):
	vo = {
		'xmin':o.point_min.x, 
		'ymin':o.point_min.y, 
		'xmax':o.point_max.x, 
		'ymax':o.point_max.y 
	}
	return vo

def layer(o):
	vo = {
		'name':o.name,
		'srid':o.srid
	}
	return vo

def geometry(o):
	vo = {
		'id':o.id,
		'layerName':o.layer.name
	}
	return vo