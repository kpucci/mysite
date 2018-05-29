function setup()
{
    // When the user scrolls the page, execute myFunction
    window.onscroll = function() {myFunction()};

    // Get the navbar
    var navbar = document.getElementById("navbar");

    // Get the offset position of the navbar
    var sticky = navbar.offsetTop;

    document.getElementById("all-button").focus();
    loadAll();

    // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
    function myFunction(){
      if (window.pageYOffset >= sticky){
        navbar.classList.add("sticky")
      } else {
        navbar.classList.remove("sticky");
      }
    }

}

/**
* Makes an HTTP request
* @param {Function} method - HTTP method (GET, POST, etc.)
* @param {String} target - Resource URL
* @param {Number} retCode - Expected return code
* @param {Function} callback - Callback method to execute once request has completed
* @param {String} data - Data to send with request
*/
function makeReq(method, target, retCode, callback, data)
{
    // Create new request
    var httpRequest = new XMLHttpRequest();

	if (!httpRequest){
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

    // On state change of request, makeHandler
	httpRequest.onreadystatechange = makeHandler(httpRequest, retCode, callback);

    // Open the request
	httpRequest.open(method, target);

    // If the request contains data
	if (data){
		httpRequest.setRequestHeader('Content-Type', 'application/json');
		httpRequest.send(data);
	}else{
		httpRequest.send();
	}
}

/**
* Function to handle the reqeust
* @param {XMLHttpRequest} httpRequest
* @param {Number} retCode - Expected return code
* @param {Function} callback - Callback method
*/
function makeHandler(httpRequest, retCode, callback)
{
	function handler() {
        // If request has been completed
		if (httpRequest.readyState === XMLHttpRequest.DONE){
            // If return code is as expected
            if (httpRequest.status === retCode){
				console.log("received response text:  " + httpRequest.responseText);
				callback(httpRequest.responseText);     // Call callback method on response text
			}else if(httpRequest.status == 0){
				console.log("received response text:  " + httpRequest.responseText);
				callback(httpRequest.responseText);
			}else{
				alert("There was a problem with the request.  You'll need to refresh the page!");
				alert(httpRequest.status);
			}
		}
	}
	return handler;
}

/**
* Get project list
*/
function loadAll()
{
    // console.log("Get Categories");
	makeReq("GET", "/cats/all", 200, showProjects);
}

/**
* Get project list
*/
function loadWeb()
{
    // console.log("Get Categories");
	makeReq("GET", "/cats/web", 200, showProjects);
}

/**
* Get project list
*/
function loadEmbedded()
{
    // console.log("Get Categories");
	makeReq("GET", "/cats/embedded", 200, showProjects);
}

/**
* Get project list
*/
function loadArt()
{
    // console.log("Get Categories");
	makeReq("GET", "/cats/art", 200, showProjects);
}

function showProjects(responseText)
{
    console.log("repopulating!");
	var projects = JSON.parse(responseText);
    var viewer = document.getElementById("port-view");

    while(viewer.hasChildNodes()){
        viewer.removeChild(viewer.childNodes[0]);
    }

    if(projects.length > 0)
    {
    	var p, img_path, proj_img, proj_container, project_name;

    	for(p in projects){
            project_name = projects[p]["name"];
    		img_path = projects[p]["img"];

            proj_container = document.createElement("div");
            proj_container.className = "project-image-container animate";
            proj_container.id = project_name;

            proj_img = document.createElement("IMG");
            proj_img.src = "/static/" + img_path;
            proj_img.alt = project_name;
            proj_img.className = "project-image";

            proj_container.appendChild(proj_img);
            viewer.appendChild(proj_container);
    	}
    }

    console.log("finished!");
}

// setup load event
window.addEventListener("load", setup, true);
