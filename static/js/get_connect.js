function appendLog(str)
{
	var elem = $("<pre>");
	elem.html(str);
    if($("#command"))
        $("#command pre:nth-child(n+3)").remove()
	    $("#command").append(elem);
}

var websocket;
var websocket_state;
var local_storage;
var json_massiv;
var json_shrank_massiv;
document.addEventListener("DOMContentLoaded", function()
{
	local_storage = window['localStorage'];
	if (!local_storage)
		appendLog("Local storage is not supported");

	appendLog("Begin connection to server ...");

    var wsUri = "ws://localhost:8888/ws";
//	var wsUri = "ws://10.1.1.1/ws/";
//	var wsUri = "ws://172.16.0.190:8001/ws/";

    websocket = new WebSocket(wsUri);
    websocket.onopen = function(evt) { wsOpen(evt) };
    websocket.onclose = function(evt) {};// wsClose(evt) };
    websocket.onmessage = function(evt) { wsMessage(evt) };
    websocket.onerror = function(evt) {};// wsError(evt) };
});

function wsOpen(evt)
{
	appendLog("Opened websocket connection");
    //websocket.send("HELLO");
	websocket_state = 1;
}

function wsMessage(evt)
{
    appendLog(evt.data);
    json = JSON.parse(evt.data);
    $("#lamp").css('background', json.color);
}
