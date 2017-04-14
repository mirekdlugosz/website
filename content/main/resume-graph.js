var g = new dagreD3.graphlib.Graph().setGraph({});

function addNode(elem, par) {
	try {
		var elemdesc = elem.getElementsByTagName("span")[0].textContent;
	} catch (e) { return }
	nodenum = nodenum + 1;
	var id = "node_" + nodenum;

	elem.setAttribute("id", id);

	g.setNode(elemdesc, {
		"label": elemdesc, 
		"shape": "circle",
		"ref": id,
	});

	var url = elem.firstChild.getAttribute("href");
	if (url)
		g.node(elemdesc).url = url;

	if (par) {
		g.setEdge(par, elemdesc, {"label": "" });
	}

	var children = elem.getElementsByTagName("ul")[0]
	if (children) {
		children = children.childNodes;
		for (var i = 0, l=children.length; i<l; ++i) {
			var child = children[i];
			if (child.nodeType === 1 && child.tagName.toUpperCase() === "LI") {
				addNode(child, elemdesc)
			}
		}
	}
}

var resume = document.getElementById("resume"),
	nodenum = 0;
addNode(resume.getElementsByTagName("li")[0])

/* FIXME: figure out why this would be needed at all
g.nodes().forEach(function(v) {
		var node = g.node(v);
});
*/

var svg = d3.select("svg"),
	inner = svg.select("g");

/* FIXME: refresh on window size change? */
var height = window.innerHeight - 20, 
	width = window.innerWidth - 20;

svg.style({
	"height": height + "px",
	"width": width + "px"
})

var render = new dagreD3.render();

render(inner, g);

var currentScale = 3;
var centered;
var zoom = d3.behavior.zoom()
	.scaleExtent([0.7,4])
	.translate(	function() { 
		var d = g.nodes()[0],
			x = window.innerWidth / 2 - g.node(d).x * currentScale,
			y = window.innerHeight/ 2 - g.node(d).y * currentScale;
		return [x, y]
		}() )
	.scale(currentScale)
	.on("zoom", zoomed);
zoom.event(svg);
svg.call(zoom);

var instructions = document.getElementById("instructions");
instructions.style.opacity = 1;

d3.selectAll("g.nodes > g.node").on("click", function(d, i) {
	if (g.node(d).url)
		window.open(window.location.origin + g.node(d).url, "_blank").focus();
	
	scrollTo(d, i);
	showPopup( document.getElementById(g.node(d).ref) );
}, true)

svg.on("click", function(){
	hideInstructions();
	hidePopup();
}, true);

d3.select(document.getElementById("changeview")).on("click", changeview, true);

d3.select(document.body).attr("class", "graph")

function scrollTo(d, i) {
	//d3.event.stopPropagation();
	if (!d || centered === d) {
		centered = null;
	} else {
		var x = window.innerWidth / 2 - g.node(d).x * currentScale,
			y = window.innerHeight/ 2 - g.node(d).y * currentScale,
			centered = d;
	}

	inner.transition()
		.attr("transform", "translate("+ x +","+ y +")" +
			"scale("+ currentScale +")");
	zoom.translate([x,y]);
}

function showPopup(elem) {
	hidePopup();
	var children = elem.childNodes,
		extended;
	for (var i = 0, l=children.length; i<l; ++i) {
		var child = children[i];
		if (child.nodeType === 1 && child.tagName.toUpperCase() === "DIV") {
			extended = child;
			break;
		}
	}

	if (! extended) 
		return;
	
	var popup = document.getElementById("popup"),
		popupContent = extended.cloneNode(true);
	popup.style.left = Math.round(width / 2) - 40 + "px";
	popup.style.top = Math.round(height / 2) - 40 + "px";
	popup.style.width = 0;
	popup.style.height = 0;
	popup.style.margin = 0;
	popup.style.padding = 0;

	popup.appendChild(popupContent);

	var maxSize = Math.round( Math.max(popupContent.getBoundingClientRect().height, popupContent.getBoundingClientRect().width) );
	maxSize = Math.min(maxSize, height - 40*2, width - 40*2);
	popupContent.style.width  = maxSize + "px";
	popupContent.style.height = maxSize + "px";

	d3.select(popup)
		.attr("class", "visible")
		.transition()
		.style({
			"width": maxSize + "px",
			"height": maxSize + "px",
			"margin": -1 * Math.round(maxSize / 2) + "px",
			"padding": "40px",
		})
}

function hideInstructions() {
	if (!instructions || !instructions.parentNode)
		return;

	if (instructions.style.opacity == 0) {
		instructions.parentNode.removeChild(instructions);
	} else {
		d3.select(instructions)
			.transition(1000)
			.style({
				"opacity": 0,
			});
	}
}


function hidePopup() {
	var popup = document.getElementById("popup"),
		todelete = popup.childNodes[0];
	
	if (! todelete)
		return;

	popup.removeChild(todelete);

	d3.select(popup)
		.attr("class", "")
		.transition()
		.duration(100)
		.style({
			"width": 0 + "px",
			"height": 0 + "px",
			"margin": 0 + "px",
			"padding": 0 + "px",
		})
}

function zoomed() {
	hidePopup();
	inner
		.attr("transform", "translate(" + d3.event.translate + ")" + 
			"scale(" + d3.event.scale + ")");
	currentScale = d3.event.scale;
}

function changeview() {
	d3.select(document.body).attr("class", "basic")
}
