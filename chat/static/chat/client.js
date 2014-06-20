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
        if (typeof data['all_clients'] !== 'undefined') {
            var ul = $('.users ul');
            for (var client in data['all_clients']) {
                var user = data['all_clients'][client];
                if ( ! $('[data-chat=' + user + ']').length) {
                    ul.append('<li data-chat="' + user + '">' + user + '</li>');
                }
            }
        } else if (typeof data['connection_status'] !== 'undefined') {
            $('#connection_status').html('connected...');
        } else if (typeof data['username_changed'] !== 'undefined') {
            var li = $('[data-chat=' + data['username_changed'].old + ']');
            li.html(data['username_changed'].new);
            li.attr('data-chat', data['username_changed'].new);
          
        } else if (typeof data['client_lost'] !== 'undefined') {
            $('[data-chat=' + data['client_lost'] + ']').remove();
        } else {
            board.append(
                    '<div class="message well">' + 
                    '<span class="sender">' + data.sender + '</span>' + 
                    '<span class="msg">' + data.msg + '</span>' + 
                    '<span class="time">' + data.time + '</span>' + 
                    '</div>'
            );
            var height = board[0].scrollHeight;
            board.scrollTop(height);
        }
    };
});