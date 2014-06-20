/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var collapseBtn = $('.button-collapse button'),
    chatPanel   = $('.chat'),
    toLeft      = localStorage.getItem('toLeft');

if (toLeft !== null) {
    toLeft = JSON.parse(toLeft);
    console.log(toLeft)
    chatPanel.css({'left': (toLeft) ? "0%" : "-46%"});
    if (toLeft) {
        collapseBtn.removeClass('fa-angle-double-right');
        collapseBtn.addClass('fa-angle-double-left');
    } else {
        collapseBtn.removeClass('fa-angle-double-left');
        collapseBtn.addClass('fa-angle-double-right');
    }
}

collapseBtn.bind('click', function(e) {
    var toLeft = collapseBtn.hasClass('fa-angle-double-right');

    chatPanel.animate({
        left: (toLeft) ? "0%" : "-46%",
    }, 2000, function() {
        if (toLeft) {
            collapseBtn.removeClass('fa-angle-double-right');
            collapseBtn.addClass('fa-angle-double-left');
        } else {
            collapseBtn.removeClass('fa-angle-double-left');
            collapseBtn.addClass('fa-angle-double-right');
        }
        console.log(toLeft)
        localStorage.setItem('toLeft', toLeft);
        console.log(localStorage.getItem('toLeft'));
    });
});