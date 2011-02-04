# Overview

This code was originally forked and port from a GIS-WEB C# Project (WCF) to Python (mod_wsgi)  ... the purpose is 
just get abstract and generic access to postgres/postgis geometry functions from web(rest) including a Javascript API.

* The server python library is compatible with Python 2.7. adn its working with mod_wsgi (http://code.google.com/p/modwsgi/)_

# Example Client / Javascript API


	# first, include the ext-core library
	<script src="your-app-path/ext-core.js" type="text/javascript" charset="utf-8"></script>
	
	# NOTE: the geo-core javascript library will work OK with the current extjs app or sencha touch app.. 
	# more info about Sencha Products on www.sencha.com
	
    # then include the geo-core javascript library, something like this
    <script type="text/javascript" charset="utf-8" src="your-app-path/geo-core.js"></script>
    
    # set the SERVER variable 
	SERVER = 'http://your-domain/mod_wsgi_server_path'
	
	# the code code looks like this ..
	
	//layer: getting pre-calculated 'spherical mercator' bbox of a single layer
	
	var layerName = 'public.my_layer'
    var l = new Geo.core.Layer();
	l.on('staticbbox', function(bbox){ 
		alert(bbox.xmin);
		//wherever !! 
	},this);
	l.getStaticBBox(layerName, 32719);
	
	//group of layers: getting pre-calculated 'spherical mercator' single bbox of N-layers
	
	var vo = {
		layers : [{name:'public.layer_1'},{name:'public.layer_1'}]
	};
	
	var g = new Geo.core.Group();
	g.on('staticbbox', function(bbox){ 
		alert(bbox.xmin);
		//wherever !! 
	},this);
	g.getStaticBbox(vo);




