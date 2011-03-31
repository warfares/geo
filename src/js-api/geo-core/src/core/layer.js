// TODO add SRID .. on call 

Ext.ns("Geo.core");
Geo.core.Layer = Ext.extend(Ext.util.Observable, {
	constructor: function (config) {
		this.addEvents(
			'query',
			'metadata',
			'bbox',
			'staticbbox'
		);
		Geo.core.Layer.superclass.constructor.call(config);
	}
	,
	query:function(layer, fields, criteria, paging, start, limit, wkt){
		paging = paging || false;
		start = start || 0;
		limit = limit || 0;
		wkt = wkt || false; 
		
		var params = {
			paging : paging,
			start : start,
			limit : limit,
			layer : layer,
			fields : fields,
			criteria : criteria,
			wkt:wkt
		};

		Ext.Ajax.request({
			url: Geo.UriTemplate.getUri('layerQuery'),
			method: 'Post',
			headers: { 'Content-Type': 'text/json' },
			jsonData: params,
			scope: this,
			success: function (response, options) {
				var result = Ext.util.JSON.decode(response.responseText);
				this.fireEvent('query', result);
			}
		});
	}
	,
	getMetadata:function(layer){
		Ext.Ajax.request({
			url: Geo.UriTemplate.getUri('layer', layer + '/metadata'),
			method: 'Get',
			headers: { 'Content-Type': 'text/json' },
			scope:this,
			success: function (response, options) {
				var result = Ext.util.JSON.decode(response.responseText);
				this.fireEvent('metadata', result);
			}
		});
	}
	,
	getBBox:function(layer){
		Ext.Ajax.request({
			url: Geo.UriTemplate.getUri('layer', layer + '/bbox'),
			method: 'Get',
			headers: { 'Content-Type': 'text/json' },
			scope:this,
			success: function (response, options) {
				var result = Ext.util.JSON.decode(response.responseText);
				this.fireEvent('bbox', result);
			}
		});
	}
	,
	getStaticBBox:function(layer){
		Ext.Ajax.request({
			url: Geo.UriTemplate.getUri('layer', layer + '/staticbbox'),
			method: 'Get',
			headers: { 'Content-Type': 'text/json' },
			scope:this,
			success: function (response, options) {
				var result = Ext.util.JSON.decode(response.responseText);
				this.fireEvent('staticbbox', result);
			}
		});
	}
});