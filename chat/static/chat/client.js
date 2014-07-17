$(document).ready(function () {
    var disconnectBtn   = $('#disconnect-button'),
        connectBtn      = $('#connect-button');

    disconnectBtn.hide();
    connectBtn.bind('click', function () {
        $(this).hide();
        disconnectBtn.show();
        var socket  = new WebSocket('ws://' + window.location.hostname + ':1025/ws'),
            board   = $('#message_list'),
            input   = $('#send-text'),
            sendBtn = $('#send-button'),
            audio   = new Audio('/static/chat/sound.mp3');
        disconnectBtn.bind('click', function () {
            $(this).hide();
            connectBtn.show();
            socket.close();
        });
        var tabController = function () {
            $('[name=user]').unbind('click');
            $('[name=user]').bind('click', function () {
                var userName = $(this).html();
                if ($('#message_list' + userName).length === 0 && userName !== $('#author').html()) {
                    $('#chat-tabs').append(
                        '<li name ="' + userName + '">' + 
                        '<a href="#' + userName + '" data-toggle="tab">' + 
                        userName +
                        '<button data="' + userName + '" name="close-tab" class="btn btn-xs btn-danger btn-close pull-right">x</button>' +
                        '</a>' + 
                        '</li>'
                    );
                    var panelTemplate = '<div class="message-list" id="message_list' + userName + '"></div>' +
                    '<div class="controls row">' +
                        '<div class="col-md-8">' +
                            '<input class="form-control" id="send-text' + 
                            userName + '" type="text" user="' + userName + '" />' +
                        '</div>' +
                        '<div class="col-md-4">' +
                            '<button class="btn btn-info" id="send-button' + userName + '">Wyślij <i class="fa fa-send"></i></button>' +
                        '</div>' +
                    '</div>';
                    $('#chat-panel').append(
                        '<div class="tab-pane fade" id="' + userName + '">' + panelTemplate + '</div>'
                    );
                    $('[name=close-tab]').bind('click', function() {
                        var userName = $(this).attr('data');
                        $('div#' + userName).remove();
                        $('[data=' + userName + ']').closest('li').remove();
                    });

                    var inputUser   = $('#send-text' + userName),
                        sendBtnUser = $('#send-button' + userName);

                    sendBtnUser.unbind('click');
                    sendBtnUser.bind('click', function(e) {
                        var e = jQuery.Event('keypress');
                        e.which = 13;
                        inputUser.trigger(e);
                    });
                    inputUser.unbind('keypress');
                    inputUser.bind('keypress', function(e) {
                        var code = e.keyCode || e.which;
                        if (code == 13) { //Enter keycode
                            var me  = $(this),
                                msg = JSON.stringify({
                                    'prvMsg':me.val(),
                                    'receiver': $(this).attr('user')
                                });
                            socket.send(msg);
                            me.val('');
                        }
                    });
                }
            });
        };
        function parseEmoticons (msg) {
            var bin = {
                ':)': '<img src="/static/chat/emoticon/Smile.png"/>',
                '*smile*': '<img src="/static/chat/emoticon/Smile.png"/>',
                ':*': '<img src="/static/chat/emoticon/Kiss.png"/>'

            };
            for (var i in bin) {
                msg = msg.split(i).join(bin[i]);
            }
            return msg;
        };
        
        sendBtn.unbind('click');
        sendBtn.bind('click', function(e) {
            var e = jQuery.Event('keypress');
            e.which = 13;
            input.trigger(e);
        });
        input.unbind('keypress');
        input.bind('keypress', function(e) {
            var code = e.keyCode || e.which;
            if (code == 13) { //Enter keycode
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
                if ($('#author').html() === data['username_changed'].old) {
                    $('#author').html(data['username_changed'].new);
                }
                var li = $('[data-chat=' + data['username_changed'].old + ']');
                li.html('<button name="user">' + data['username_changed'].new + '</button>');
                li.attr('data-chat', data['username_changed'].new);

            } else if (typeof data['client_lost'] !== 'undefined') {
                $('[data-chat=' + data['client_lost'] + ']').remove();
            } else if (typeof data['prvMsg'] !== 'undefined') {
                var author = $('#author').html();
                $('.users [name=user]').each(function () {
                    var me = $(this);
                    if (me.html() === data.receiver && data.sender === author) {
                        me.trigger('click');
                        var boardUser = $('#message_list' + data.receiver);
                        
                        var classAuthor = 'author';
                        boardUser.append(
                            '<div class="message well">' + 
                            '<span class="sender ' + classAuthor + '">' + 
                            '<button name="user">' + data.sender + '</button>' + 
                            '</span>' + 
                            '<span class="msg">' + parseEmoticons(data.prvMsg) + '</span>' + 
                            '<span class="time">' + data.time + '</span>' + 
                            '</div>'
                        );
                        var height = boardUser[0].scrollHeight;
                        boardUser.scrollTop(height);
                    } else if (me.html() === data.sender && data.sender !== author) {
                        me.trigger('click');
                        var boardUser = $('#message_list' + data.sender);
                        
                        boardUser.append(
                            '<div class="message well">' + 
                            '<span class="sender ">' + 
                            '<button name="user">' + data.sender + '</button>' + 
                            '</span>' + 
                            '<span class="msg">' + parseEmoticons(data.prvMsg) + '</span>' + 
                            '<span class="time">' + data.time + '</span>' + 
                            '</div>'
                        );
                        var height = boardUser[0].scrollHeight,
                            useSound = JSON.parse(localStorage.getItem('useSound')),
                            tab = $('#chat-tabs [name=' + data.sender + ']');
                        if ( ! tab.hasClass('active')) {
                            tab.addClass('new-msg');
                            tab.unbind('click');
                            tab.bind('click', function() {
                                $(this).removeClass('new-msg');
                            });
                        }
                        boardUser.scrollTop(height);
                        if (useSound !== false) {
                            audio.play();
                        }
                    }
                });
                
            }else {
                var classAuthor = (data.receiver === data.sender) ? 'author' : '';

                board.append(
                        '<div class="message well">' + 
                        '<span class="sender ' + classAuthor + '">' + 
                        '<button name="user">' + data.sender + '</button>' + 
                        '</span>' + 
                        '<span class="msg">' + parseEmoticons(data.msg) + '</span>' + 
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
        
        socket.onclose = function () {
            $('#connection_status').html('rozłączono...');
            $('.users ul li').remove();
            $('#message_list .message').remove();
        };
    });
});