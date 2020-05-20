(function($){ 
	'use strict';
	$('.stellarnav').stellarNav({
		theme: 'light',
        breakpoint: 960,
        position: 'right',
        menuLabel: '<i class="fa fa-bars"></i>',
        closeLabel: '<i class="fa fa-close"></i>'
	});

	$(".sm-featured-slider").owlCarousel({
		items: 3,
		margin: 30,
		nav: true,
		loop: true,
		responsive: {
            0: {
                items: 1,
                nav: false,
                margin: 20
            },
            600: {
                items: 2,
                nav: false
            },
            1000: {
                items: 3,
                nav: false,
            }
        }
	});

    var selectSubMenu = $('.footer-widget-area ul.menu li > ul');

    if (selectSubMenu.hasClass('sub-menu')) {
       $('.footer-widget-area ul.menu').addClass('removesubmenu');
    }
    
})(jQuery);