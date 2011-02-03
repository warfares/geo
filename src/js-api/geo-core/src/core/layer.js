// TODO add SRID .. on call 

Ext.ns("Geo.Core");
Geo.Core.Layer = Ext.extend(Ext.util.Observable, {
	constructor: function (config) {
		this.addEvents(
			'query',
			'metadata',
			'bbox',
			'staticbbox'
		);
		Geo.Core.Layer.superclass.constructor.call(config);
	}
	,
	query:function(layer, fields, criteria){
		var params = {
			layer : layer,
			fields : fields,
			criteria : criteria
		};

		Ext.Ajax.request({
			url: Geo.UriTemplate.getUri('layer_query'),
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