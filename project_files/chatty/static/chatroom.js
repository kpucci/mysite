var timeoutID;
var timeout = 1000;
var boxHeight;
var oldBoxHeight;
// var lasttime;

// NOTE: To make it so only new messages are sent to the user, make the posttime
// property of message in resources, get the current time in the chatroom using
// JS, and only receive messages after that time.

// NOTE: To ensure a user is only in one room at a time, need to add a users
// property to the ChatRoom model (making it a many-to-many relationship), and
// then checking if the user is a part of any other rooms before allowing them in

function setup()
{
    // requestMessageHistory();
    // Assign event listener to new-message-button
	document.getElementById("new-message-button").addEventListener("click", addMessage, true);
    // Assign event listener to new-message-text for Enter key
    document.getElementById("new-message-text").addEventListener("keydown", function(e) {

        // Enter is pressed
        if (e.keyCode == 13) {
            e.preventDefault();
            addMessage(); }
        }, false);

    // Get chatroom name from chatroom-name header
    var chatroom = document.getElementById("chatroom-name").textContent;

    // If the person signed in is the chatroom creator, create a delete button

    if(document.getElementById("new-message-button").value == document.getElementById("logout-button").value)
    {
        var deleteButton = document.createElement("button");
        deleteButton.value = chatroom;
  		deleteButton.innerHTML = "Delete Chatroom";
  		deleteButton.id = "delete-button";
        deleteButton.name = "delete-button";
        deleteButton.className = "form-button";
        deleteButton.type = "button";
        deleteButton.addEventListener("click", deleteChatRoom, true);
        document.getElementById("logout-div").appendChild(deleteButton);
    }

    // Start polling
	poller();
}

function addMessage()
{
    // Get new message text
	var newMessage = document.getElementById("new-message-text").value;

    // Get user from logout-button value
	var current_user = document.getElementById("logout-button").value;

    // Get chatroom name from chatroom-name header
	var chatroom = document.getElementById("chatroom-name").textContent;

    // Create data for new message
	var data;
	data = '{"creator":"' + current_user + '","text":"' + newMessage + '","chatroom":"' + chatroom + '"}';

    // Clear the timeout
    window.clearTimeout(timeoutID);

    // Make the post request
	makeReq("POST", "/messages/"+chatroom, 201, poller, data);
	document.getElementById("new-message-text").value = "";

}

function deleteChatRoom()
{
    var chatroom = document.getElementById("chatroom-name").textContent;
    makeReq("DELETE", "/chatrooms/"+chatroom, 204, reloadAccount);
}

function reloadAccount()
{
    var current_user = document.getElementById("logout-button").value;
    window.location.href = "/account/" + current_user;
}

function reloadAccount2()
{
    var current_user = document.getElementById("logout-button").value;
    alert("This chatroom has been deleted by the creator.");
    window.location.href = "/account/" + current_user;
}

function makeReq(method, target, retCode, callback, data)
{
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest)
    {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = makeHandler(httpRequest, retCode, callback);

	httpRequest.open(method, target);

	if (data)
    {
		httpRequest.setRequestHeader('Content-Type', 'application/json');
		httpRequest.send(data);
	}
	else
    {
		httpRequest.send();
	}
}

function makeHandler(httpRequest, retCode, callback)
{
	function handler() {
		if (httpRequest.readyState === XMLHttpRequest.DONE)
        {
			if (httpRequest.status === retCode)
            {
				console.log("recieved response text:  " + httpRequest.responseText);
				callback(httpRequest.responseText);
			}
			else if(httpRequest.status == 0)
			{
				console.log("recieved response text:  " + httpRequest.responseText);
				callback(httpRequest.responseText);
			}
			else
            {
				alert("There was a problem with the request.  You'll need to refresh the page!");
				alert(httpRequest.status);
			}
		}
	}
	return handler;
}

function poller() {
	chatroom = document.getElementById("chatroom-name").textContent;
	makeReq("GET", "/messages/"+chatroom, 200, repopulate);
}

function addUserCell(row, text) {
	var newCell = row.insertCell();
	var newText = document.createTextNode(text);
	newCell.appendChild(newText);
	newCell.className = "username-cell";
}

function addTextCell(row, text) {
	var newCell = row.insertCell();
	var newDiv = document.createElement("div");
	newDiv.className = "text-bubble";
	var newText = document.createTextNode(text);
	newDiv.appendChild(newText);
	newCell.appendChild(newDiv);
	newCell.className = "text-cell";
}

function addTextCellCurrentUser(row, text) {
	var newCell = row.insertCell();
	var newDiv = document.createElement("div");
	newDiv.className = "text-bubble-current";
	var newText = document.createTextNode(text);
	newDiv.appendChild(newText);
	newCell.appendChild(newDiv);
	newCell.className = "current-user-text-cell";
	newCell.colSpan = "2";
}

function addBlankCell(row, colspan) {
	var newCell = row.insertCell();
	newCell.className = "blank-cell";
	newCell.colSpan = colspan;
}

// function requestMessageHistory() {
// 	chatroom = document.getElementById("chatroom-name").textContent;
// 	makeReq("GET", "/history/"+chatroom, 200, loadMessageHistory);
// }

// function loadMessageHistory(responseText) {
//     console.log("repopulating!");
// 	var messages = JSON.parse(responseText);
//
//     // Check if deleted
//     if(messages.length == undefined)
//     {
//         reloadAccount2();
//     }
//
//     if(messages.length > 0)
//     {
//     	var tab = document.getElementById("message-table");
//     	var newRow, m, message;
//
//     	while (tab.rows.length > 0) {
//     		tab.deleteRow(0);
//     	}
//
//     	var current_user = document.getElementById("logout-button").value;
//     	var message_creator;
//     	for (m in messages) {
//     		newRow = tab.insertRow();
//     		message_creator = messages[m]["creator"];
//             if(message_creator == null)
//             {
//                 reloadAccount2();
//             }
//             else if(message_creator == current_user)
//     		{
//     			addBlankCell(newRow, 2);
//     			addTextCellCurrentUser(newRow, messages[m]["text"]);
//     		}
//     		else
//     		{
//     			addUserCell(newRow, messages[m]["creator"]);
//     			addTextCell(newRow, messages[m]["text"]);
//     			addBlankCell(newRow, 1);
//     		}
//
//     	}
//     	var tableDiv = document.getElementById("table-container");
//
//     	boxHeight = tableDiv.scrollHeight;
//
//     	if(boxHeight != oldBoxHeight)
//     	{
//     		oldBoxHeight = boxHeight;
//     		tableDiv.scrollTop = tableDiv.scrollHeight - tableDiv.clientHeight;
//     	}
//     }
//     var d = new Date();
//     var day = d.getDate();
//     var year = d.getFullYear();
//     var month = d.getMonth() + 1;
//     var hour = d.getHours();
//     var minute = d.getMinutes();
//     var second = d.getSeconds();
//     var millisecond = d.getMilliseconds();
//     lasttime = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second + '.' + millisecond;
//     timeoutID = window.setTimeout(poller, timeout);
// }

function repopulate(responseText) {
    console.log("repopulating!");
	var messages = JSON.parse(responseText);

    // Check if deleted
    if(messages.length == undefined)
    {
        reloadAccount2();
    }

    if(messages.length > 0)
    {
    	var tab = document.getElementById("message-table");
    	var newRow, m, message;

    	while (tab.rows.length > 0) {
    		tab.deleteRow(0);
    	}

    	var current_user = document.getElementById("logout-button").value;
    	var message_creator;
    	for (m in messages) {
    		newRow = tab.insertRow();
    		message_creator = messages[m]["creator"];
            if(message_creator == null)
            {
                reloadAccount2();
            }
            else if(message_creator == current_user)
    		{
    			addBlankCell(newRow, 2);
    			addTextCellCurrentUser(newRow, messages[m]["text"]);
    		}
    		else
    		{
    			addUserCell(newRow, messages[m]["creator"]);
    			addTextCell(newRow, messages[m]["text"]);
    			addBlankCell(newRow, 1);
    		}

    	}
    	var tableDiv = document.getElementById("table-container");

    	boxHeight = tableDiv.scrollHeight;

    	if(boxHeight != oldBoxHeight)
    	{
    		oldBoxHeight = boxHeight;
    		tableDiv.scrollTop = tableDiv.scrollHeight - tableDiv.clientHeight;
    	}
    }

	timeoutID = window.setTimeout(poller, timeout);

}

// setup load event
window.addEventListener("load", setup, true);
