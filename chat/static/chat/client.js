$(document).ready(function () {

    var socket  = new WebSocket('ws://' + window.location.hostname + ':1025/ws'),
        board   = $('#message_list'),
        input   = $('#send-text'),
        sendBtn = $('#send-button'),
        audio   = new Audio('/static/chat/sound.mp3');
        
    var tabController = function () {
        $('[name=user]').bind('click', function () {
            var userName = $(this).html();
            $('#chat-tabs').append(
                '<li><a href="#' + userName + '" data-toggle="tab">' + 
                userName + 
                '<button data="' + userName + '" name="close-tab" class="btn btn-xs btn-danger pull-right">x</button>' +
                '</a></li>'
            );
            $('#chat-panel').append(
                '<div class="tab-pane fade" id="' + userName + '"></div>'
            );
            $('[name=close-tab]').bind('click', function() {
                var userName = $(this).attr('data');
                $('div#' + userName).remove();
                $('[data=' + userName + ']').closest('li').remove();
            });
        });
    };


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
            var ul = $('.users ul'),
                author = $('#author').html(),
                classAuthor = '';
        
            for (var client in data['all_clients']) {
                var user = data['all_clients'][client];
                if ( ! $('[data-chat=' + user + ']').length) {
                    if (user === author) classAuthor = 'author';
                    ul.append(
                        '<li class="' + classAuthor + '" data-chat="' + user + '">' + 
                        '<button name="user">' + user + '</button>' +
                        '</li>'
                    );
                    classAuthor = '';
                }
            }
        } else if (typeof data['connection_status'] !== 'undefined') {
            $('#connection_status').html('połączono...');
            $('#author').html(data['you']);
        } else if (typeof data['username_changed'] !== 'undefined') {
            var li = $('[data-chat=' + data['username_changed'].old + ']');
            $('#author').html(data['username_changed'].new);
            li.html('<button name="user">' + data['username_changed'].new + '</button>');
            li.attr('data-chat', data['username_changed'].new);
          
        } else if (typeof data['client_lost'] !== 'undefined') {
            $('[data-chat=' + data['client_lost'] + ']').remove();
        } else {
            var classAuthor = (data.receiver === data.sender) ? 'author' : '';
           
            board.append(
                    '<div class="message well">' + 
                    '<span class="sender ' + classAuthor + '">' + 
                    '<button name="user">' + data.sender + '</button>' + 
                    '</span>' + 
                    '<span class="msg">' + data.msg + '</span>' + 
                    '<span class="time">' + data.time + '</span>' + 
                    '</div>'
            );

            var height = board[0].scrollHeight,
                useSound = JSON.parse(localStorage.getItem('useSound'));
            board.scrollTop(height);
            if (data.sender !== data.receiver) {
                if (useSound !== false) {
                    audio.play();
                }
            }
        }
        tabController();
    };
});