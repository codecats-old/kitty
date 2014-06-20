$(document).ready(function () {

    var socket  = new WebSocket('ws://' + window.location.hostname + ':1025/ws'),
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

    socket.onopen = function () {
        this.send(JSON.stringify({'key':$('[name=chat-key]').text()}));
    };

    socket.onmessage = function (event) {
        var data = JSON.parse(event.data);
        console.log(data);
        if (typeof data['all_clients'] !== 'undefined') {
            var ul = $('.users ul');
            for (var client in data['all_clients']) {
                var user = data['all_clients'][client];
                ul.append('<li data-chat="' + user + '">' + user + '</li>');
            }
        } else if (typeof data['connection_status'] !== 'undefined') {
            $('#connection_status').html('connected...');
        } else if (typeof data['username_changed'] !== 'undefined') {
            
        } else {
            
            board.append(
                    '<div class="message">' + data.msg + 
                    '<span>' + data.time + '</span>' + 
                    '</div>');
        }
    };
});