(function() {
		var jsfiles = new Array(
			'uriTemplate.js',
			'core/group.js',
			'core/layer.js',
		); // files 

		var agent = navigator.userAgent;
		var docWrite = (agent.match("MSIE") || agent.match("Safari"));
		if(docWrite) {
			var allScriptTags = new Array(jsfiles.length);
		}
		var host = "js/libs/geo-core-1.0.0/";
		
		for (var i=0, len=jsfiles.length; i<len; i++) {
			if (docWrite) {
				allScriptTags[i] = "<script src='" + host + jsfiles[i] + "'></script>";
			} else {
				var s = document.createElement("script");
				s.src = host + jsfiles[i];
				var h = document.getElementsByTagName("head").length ?
				document.getElementsByTagName("head")[0] : 
				document.body;
				h.appendChild(s);
			}
		}
		if (docWrite) {
			document.write(allScriptTags.join(""));
		}
	}
)();