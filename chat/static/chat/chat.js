/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var collapseBtn = $('.button-collapse button'),
    chatPanel   = $('.chat'),
    toLeft      = localStorage.getItem('toLeft'),
    soundBtn    = $('#sound-button'),
    useSound    = JSON.parse(localStorage.getItem('useSound'));

if (toLeft !== null) {
    toLeft = JSON.parse(toLeft);
    chatPanel.css({'left': (toLeft) ? "0%" : "-46%"});
    if (toLeft) {
        collapseBtn.removeClass('fa-angle-double-right');
        collapseBtn.addClass('fa-angle-double-left');
    } else {
        collapseBtn.removeClass('fa-angle-double-left');
        collapseBtn.addClass('fa-angle-double-right');
    }
}

if (useSound === false) {
    soundBtn.addClass('fa-microphone-slash');
} else {
    soundBtn.removeClass('fa-microphone-slash');
}

collapseBtn.bind('click', function(e) {
    var toLeft = collapseBtn.hasClass('fa-angle-double-right');

    chatPanel.animate({
        left: (toLeft) ? "0%" : "-46%",
    }, 1000, function() {
        if (toLeft) {
            collapseBtn.removeClass('fa-angle-double-right');
            collapseBtn.addClass('fa-angle-double-left');
        } else {
            collapseBtn.removeClass('fa-angle-double-left');
            collapseBtn.addClass('fa-angle-double-right');
        }
        localStorage.setItem('toLeft', toLeft);
    });
});

soundBtn.bind('click', function(e) {
    useSound = ! useSound;
    localStorage.setItem('useSound', useSound);
    
    if (useSound === false) {
        soundBtn.addClass('fa-microphone-slash');
    } else {
        soundBtn.removeClass('fa-microphone-slash');
    }
});