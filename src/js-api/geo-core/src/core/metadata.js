Ext.ns("Geo.core");
Geo.core.Metadata = Ext.extend(Ext.util.Observable, {
	constructor: function (config) {
		this.addEvents(
			'distinct_values'
		);
		Geo.core.Metadata.superclass.constructor.call(config);
	}
	,
	getDistinctValues:function(name, layer, limit){

		var p = {
			name : name,
			layer : layer,
			limit : limit
		};

		Ext.Ajax.request({
			url: Geo.UriTemplate.getUri('metadataDistinctValues', '?' + Ext.urlEncode(p)),
			method: 'Get',
			headers: { 'Content-Type': 'text/json' },
			scope: this,
			success: function (response, options) {
				var result = Ext.util.JSON.decode(response.responseText);
				this.fireEvent('distinct_values', result);
			}
		});
	}
});