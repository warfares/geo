Ext.ns("Geo.core");
Geo.core.Group = Ext.extend(Ext.util.Observable, {
	constructor: function (config) {
		this.addEvents(
			'staticbbox',
			'withinpoint',
			'withinbbox',
			'closestpoint'
		);
		Geo.core.Group.superclass.constructor.call(config);
	}
	,
	getStaticBBox:function(layers){
		var params = {
			layers: layers
		};
		
		Ext.Ajax.request({
			url: Geo.UriTemplate.getUri('group_static_bbox'),
			method: 'Post',
			headers: { 'Content-Type': 'text/json' },
			jsonData: params,
			scope:this,
			success: function (response, options) {
				var result = Ext.util.JSON.decode(response.responseText);
				this.fireEvent('staticbbox', result);
			}
		});
	}
	,
	getWithInPoint: function (layers, fields, point, dist) {
		var params = {
			layers: layers,
			fields: fields,
			point: point,
			dist: dist
		};
		
		Ext.Ajax.request({
			url: Geo.UriTemplate.getUri('group_within_point'),
			method: 'Post',
			headers: { 'Content-Type': 'text/json' },
			jsonData: params,
			scope: this,
			success: function (response, options) {
				var result = Ext.util.JSON.decode(response.responseText);
				this.fireEvent('withinpoint', result);
			}
		});
	}
	,
	getWithInBBox: function (layers, bbox) {
		var params = {
			layers: layers,
			bbox: bbox
		};
		Ext.Ajax.request({
			url: Geo.UriTemplate.getUri('group_within_bbox'),
			method: 'Post',
			headers: { 'Content-Type': 'text/json' },
			jsonData: params,
			scope: this,
			success: function (response, options) {
				var result = Ext.util.JSON.decode(response.responseText);
				this.fireEvent('withinbbox', result);
			}
		});
	}
	,
	getClosestPoint: function (layers, point) {
		var params = {
			layers: layers,
			point: point
		};
		
		Ext.Ajax.request({
			url: Geo.UriTemplate.getUri('group_closest_point'),
			method: 'Post',
			headers: { 'Content-Type': 'text/json' },
			jsonData: params,
			scope: this,
			success: function (response, options) {
				var result = Ext.util.JSON.decode(response.responseText);
				this.fireEvent('closestpoint', result.points);
			}
		});
	}
});

