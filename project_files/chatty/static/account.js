var timeoutID;
var timeout = 5000;

function setup()
{
	document.getElementById("new-chatroom-button").addEventListener("click", addChatRoom, true);
    document.getElementById("new-chatroom-name").addEventListener("keydown", function(e) {

    // Enter is pressed
    if (e.keyCode == 13) {
        e.preventDefault();
        addChatRoom(); }
    }, false);
	poller();
}

function addChatRoom()
{
	var newChatroom = document.getElementById("new-chatroom-name").value;
	// alert(newChatroom);
	var username = document.getElementById("new-chatroom-button").value;
	// alert(username);
	var data;
	data = '{"name":"' + newChatroom + '","creator":"' + username + '"}';
	window.clearTimeout(timeoutID);
	// alert("about to make request");
	makeReq("POST", "/chatrooms/", 201, poller, data);
	document.getElementById("new-chatroom-name").value = "";
}

function makeReq(method, target, retCode, callback, data) {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
	// alert("stop 1");
	httpRequest.onreadystatechange = makeHandler(httpRequest, retCode, callback);
	// alert("stop 2");

	httpRequest.open(method, target);
	// alert("stop 3");

	if (data){
		// alert(data);
		httpRequest.setRequestHeader('Content-Type', 'application/json');
		httpRequest.send(data);
	}
	else {
		httpRequest.send();
	}
}

function makeHandler(httpRequest, retCode, callback) {
	function handler() {
		if (httpRequest.readyState === XMLHttpRequest.DONE) {
			if (httpRequest.status === retCode) {
				console.log("recieved response text:  " + httpRequest.responseText);
				callback(httpRequest.responseText);
			} else {
				alert("There was a problem with the request.  you'll need to refresh the page!");
			}
		}
	}
	return handler;
}

function poller() {
	makeReq("GET", "/chatrooms/", 200, repopulate);
}

function deleteChatRoom(roomID) {
	makeReq("DELETE", "/chatrooms/" + roomID, 204, poller);
}

function addCell(row, text) {
	var newCell = row.insertCell();
	var newText = document.createTextNode(text);
    newCell.className = "chatroom-table-cell"
	newCell.appendChild(newText);
}

function noRoomsMessage(row)
{
    var newCell = row.insertCell();
    var newText = document.createTextNode("There are no available chatrooms.");
    newCell.className = "no-chatrooms-message";
    newCell.appendChild(newText);
}

function repopulate(responseText) {
	console.log("repopulating!");
	var rooms = JSON.parse(responseText);
	var tab = document.getElementById("chatroom-table");
	var newRow, newCell, r, room, roomname, roomname_under;

	while (tab.rows.length > 0) {
		tab.deleteRow(0);
	}

    if(rooms.length == 0)
    {
        newRow = tab.insertRow();
        noRoomsMessage(newRow);
    }
    else
    {
        for (r in rooms) {
    		newRow = tab.insertRow();
    		roomname = rooms[r]["name"];
    		addCell(newRow, "Name: " + roomname);
    		// addCell(newRow, "Creator: " + rooms[r]["creator"])

    		roomname_under = roomname.replace(/\s/, "_");

    		newCell = newRow.insertCell();
    		newButton = document.createElement("button");
    		newButton.type = "submit";
    		newButton.name = "join-chat-button";
    		newButton.value = roomname;
    		newButton.innerHTML = "Join Chatroom";
    		newButton.id = "join-chatroom-button";
    		newCell.appendChild(newButton);

    	}
    }

	timeoutID = window.setTimeout(poller, timeout);
}

// function joinRoom(room)
// {
	// makeReq("GET", "/room/"+room, 200, poller)
// }

// setup load event
window.addEventListener("load", setup, true);
