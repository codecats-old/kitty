$(document).ready(function () {
    var socket  = new WebSocket("ws://127.0.0.1:1025/ws"),
        board   = $('#message_list'),
        input   = $('#send-text'),
        sendBtn = $('#send-button');

    sendBtn.bind('click', function(e) {
        var e = jQuery.Event('keypress');
        e.which = 13;
        input.trigger(e);
    });
    input.bind('keypress', function(e) {
        var code = e.keyCode || e.which;
        if(code == 13) { //Enter keycode
            var me = $(this);
            socket.send(me.val());
            me.val('');
        }
    });

    socket.onmessage = function (event) {
        board.append('<div class="message">' + event.data + '</div>');
        console.log(event.data);
    };
});