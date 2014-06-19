$(document).ready(function () {
    var socket = new WebSocket("ws://127.0.0.1:1025/ws", "protocolOne");
    socket.onmessage = function (event) {
        console.log(event.data);
    };
});