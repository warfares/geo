# Overview.

This code was originally forked and port from a C# Project (WCF) to Python (mod_wsgi) the purpose is 
just get abstract and generic access from web(rest) to postgres/postgis geometry functions, including a Javascript API.

* The server python library is compatible with Python 2.7. and is working with mod_wsgi (http://code.google.com/p/modwsgi/)_


# Example JavaScript API.

	the code look like this ...
	
	
	<script src="your-app-path/ext-core.js" type="text/javascript" charset="utf-8"></script>
    <script src="your-app-path/geo-core.js" type="text/javascript" charset="utf-8" ></script>


	GEO_SERVER = 'http://your-domain/mod_wsgi_server_path'
	
	//bbox for a layer
	
	var layerName = 'public.my_layer'
    var l = new Geo.core.Layer();
	l.on('staticbbox', function(bbox){ 
		alert(bbox.xmin);
		//wherever !! 
	},this);
	l.getStaticBBox(layerName);
	
	//bbox for a group o layer
	
	var vo = {
		layers : [{name:'public.layer_1'},{name:'public.layer_1'}]
	};
	
	var g = new Geo.core.Group();
	g.on('staticbbox', function(bbox){ 
		alert(bbox.xmin);
		//wherever !! 
	},this);
	g.getStaticBbox(vo);


# Dependencies 
	
	server:
		python 2.7
		psycopg
		bottle  		http://bottle.paws.de/docs/dev/index.html
		
		mod_wsgi		http://code.google.com/p/modwsgi/
		
	js-api
		ext-core 		http://www.sencha.com
		


# Whish List 

	TODO: try to change the sql queries (now on the begining) for a database(postgres/postgis mysql etc..) dialect's..
	TODO: upgrade to the upcoming Sencha Products Release .
	
