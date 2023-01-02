odoo.define('iwesabe_website_theme.custom_js', function (require) {
"use strict";

$(document).ready(function() {

	$('.navbar-light .dmenu').hover(function () {
        $(this).find('.sm-menu').first().stop(true, true).slideDown(150);
    }, function () {
        $(this).find('.sm-menu').first().stop(true, true).slideUp(105)
    });
	

	$(".megamenu").on("click", function(e) {
		e.stopPropagation();
	});

	// Add to cart
	$(document).on('click', '.ian-add-cart-btn', function(){
	    var ajax = require('web.ajax');
		var variant_id = $(this).parent().find('.ian_prod_id').val();
		var qty = $(this).parent().parent().find('.ian-popup__counter-input').val();
		var add_qty = qty != undefined ? parseInt(qty) : 1
        ajax.jsonRpc("/ian/shop/add/cart", "call", {'vid': parseInt(variant_id), 'qty': add_qty})
        .then(function() {
           var cur =  $('.my_cart_quantity').text();
           var latest_count = parseInt(cur) + add_qty
           $('.my_cart_quantity').text(latest_count)
        });
        return false
	})

    // Homepage Product Slide
    $('#product_slider').slick({
        infinite: true,
        centerMode: false,
        slidesToShow: 4,
        slidesToScroll: 4,
        arrows: false,
        autoplay: true,
        autoplaySpeed: 1000,
    });

//Homepage Partner Logo Slide
//	$('.partners-logos').slick({
//		slidesToShow: 5,
//		slidesToScroll: 1,
//		autoplay: true,
//		autoplaySpeed: 1500,
//		arrows: false,
//		dots: false,
//		pauseOnHover: false,
//		responsive: [{
//			breakpoint: 768,
//			settings: {
//				slidesToShow: 4
//			}
//		}, {
//			breakpoint: 520,
//			settings: {
//				slidesToShow: 3
//			}
//		}]
//	});


$('.customer-logos').slick({
	dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 5,
    arrows: false,
	slidesToScroll: 4,
	initialSlide: 0,
    responsive: [{
        breakpoint: 768,
        settings: {
            slidesToShow: 4
        }
    }, {
        breakpoint: 520,
        settings: {
            slidesToShow: 3
        }
    }]
});

	$(".carousel-control-close").click(function(){
		$(this).hide();
		$(".newhome-slider").slideUp();
	})
});

$(document).ready(function () {
    $(".owl-theme1").owlCarousel({
        items: 3,
        loop: true,
        margin: 40,
        stagePadding: 0,
        smartSpeed: 450,
        autoplay: true,
        autoPlaySpeed: 3000,
        autoPlayTimeout: 1000,
        autoplayHoverPause: true,
        dots: false,
        nav: true,
        navText: [
        '<div class="pre"><i class="material-icons" style="font-size:36px">keyboard_arrow_left</i></div>',
        '<div class="nxt"><i class="material-icons" style="font-size:36px">keyboard_arrow_right</i></div>',
        ],
    });
});
$(document).ready(function () {
    var itemsMainDiv = ('.MultiCarousel');
    var itemsDiv = ('.MultiCarousel-inner');
    var itemWidth = "";

    $('.leftLst, .rightLst').click(function () {
        var condition = $(this).hasClass("leftLst");
        if (condition)
            click(0, this);
        else
            click(1, this)
    });

    ResCarouselSize();




    $(window).resize(function () {
        ResCarouselSize();
    });

    //this function define the size of the items
    function ResCarouselSize() {
        var incno = 0;
        var dataItems = ("data-items");
        var itemClass = ('.item');
        var id = 0;
        var btnParentSb = '';
        var itemsSplit = '';
        var sampwidth = $(itemsMainDiv).width();
        var bodyWidth = $('body').width();
        $(itemsDiv).each(function () {
            id = id + 1;
            var itemNumbers = $(this).find(itemClass).length;
            btnParentSb = $(this).parent().attr(dataItems);
            itemsSplit = btnParentSb.split(',');
            $(this).parent().attr("id", "MultiCarousel" + id);


            if (bodyWidth >= 1200) {
                incno = itemsSplit[3];
                itemWidth = sampwidth / incno;
            }
            else if (bodyWidth >= 992) {
                incno = itemsSplit[2];
                itemWidth = sampwidth / incno;
            }
            else if (bodyWidth >= 768) {
                incno = itemsSplit[1];
                itemWidth = sampwidth / incno;
            }
            else {
                incno = itemsSplit[0];
                itemWidth = sampwidth / incno;
            }
            $(this).css({ 'transform': 'translateX(0px)', 'width': itemWidth * itemNumbers });
            $(this).find(itemClass).each(function () {
                $(this).outerWidth(itemWidth);
            });

            $(".leftLst").addClass("over");
            $(".rightLst").removeClass("over");

        });
    }


    //this function used to move the items
    function ResCarousel(e, el, s) {
        var leftBtn = ('.leftLst');
        var rightBtn = ('.rightLst');
        var translateXval = '';
        var divStyle = $(el + ' ' + itemsDiv).css('transform');
        var values = divStyle.match(/-?[\d\.]+/g);
        var xds = Math.abs(values[4]);
        if (e == 0) {
            translateXval = parseInt(xds) - parseInt(itemWidth * s);
            $(el + ' ' + rightBtn).removeClass("over");

            if (translateXval <= itemWidth / 2) {
                translateXval = 0;
                $(el + ' ' + leftBtn).addClass("over");
            }
        }
        else if (e == 1) {
            var itemsCondition = $(el).find(itemsDiv).width() - $(el).width();
            translateXval = parseInt(xds) + parseInt(itemWidth * s);
            $(el + ' ' + leftBtn).removeClass("over");

            if (translateXval >= itemsCondition - itemWidth / 2) {
                translateXval = itemsCondition;
                $(el + ' ' + rightBtn).addClass("over");
            }
        }
        $(el + ' ' + itemsDiv).css('transform', 'translateX(' + -translateXval + 'px)');
    }

    //It is used to get some elements from btn
    function click(ell, ee) {
        var Parent = "#" + $(ee).parent().attr("id");
        var slide = $(Parent).attr("data-slide");
        ResCarousel(ell, Parent, slide);
    }

});

});
