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
* Makes an HTTP request
* @param {Function} method - HTTP method (GET, POST, etc.)
* @param {String} target - Resource URL
* @param {Number} retCode - Expected return code
* @param {Function} callback - Callback method to execute once request has completed
* @param {String} data - Data to send with request
* @param {String} token - Token to send with request for authorization
*/
function makeTokenReq(method, target, retCode, callback, data, token)
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
	if (data)
    {
		httpRequest.setRequestHeader('Content-Type', 'application/json');
        if(token)
            httpRequest.setRequestHeader('Authorization', 'JWT ' + token);
		httpRequest.send(data);
	}
    else
    {
        if(token)
            httpRequest.setRequestHeader('Authorization', 'JWT ' + token);
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
