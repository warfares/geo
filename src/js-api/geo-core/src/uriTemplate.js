/**
 * Geo  rest Util 
 * Simple hash table with backend rest services uri templates
 *
 * @author    (rbarriga)
 * @date      15. Junuary 2011
 * @version   1.0.0
 *
 */
Ext.ns("Geo");

Geo.WSGIScriptAlias = '';

Geo.UriTemplate = {

	groupStaticBbox: 'group/staticbbox',
	groupWithinPoint: 'group/withinpoint',
	groupWithinBbox: 'group/withinbbox',
	groupClosestPoint: 'group/closestpoint',

	layer: 'layer/',
	layerQuery : 'layer/query',
	layerBbox: 'layer/bbox',
	layerStaticBbox: 'layer/staticbbox',
	layerMetadata: 'layer/metadata',
	
	metadataDistinctValues : 'metadata/distinct_values',

	getUri: function(action, option) {
		var hostname = 'http://' + window.location.hostname + ':' + window.location.port + '/';
		return hostname + Geo.WSGIScriptAlias + '/' + Geo.UriTemplate[action] + (option || '');
	}
};  // eo Geo.Uritemplate
//eof