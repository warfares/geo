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

Geo.UriTemplate = {

	group_static_bbox: 'group/staticbbox',
	group_within_point: 'group/withinpoint',
	group_within_bbox: 'group/withinbbox',
	group_closest_point: 'group/closestpoint',

	layer: 'layer/',
	layer_query : 'layer/query',
	
	metadata_distinct_values : 'metadata/distinct_values',

	getUri: function(action, option) {
		return GEO_SERVICE + Geo.UriTemplate[action] + (option || '');
	}
};  // eo Geo.Uritemplate
// eof