/*
	Add to cart fly effect with jQuery. - May 05, 2013
	(c) 2013 @ElmahdiMahmoud - fikra-masri.by
	license: https://www.opensource.org/licenses/mit-license.php
*/
$(document).ready(function(){
    $(document).on('click', '.ian-add-cart-btn', function() {
        var cart = $('.o_wsale_my_cart');
        var prod_img;
        var anime_top = 0;
        var anime_left = 0;
        var img_top = 0;
        var img_left = 0;
        var elem = $(this).parent().parent().parent().find('.ia-product-card__image')
        var imgtodrag = 0;
        var popup_prod_img = $(this).parent().parent().parent().find('.ian-popup__product-image');
        if(elem.length > 0){
            prod_img = elem
            anime_top = cart.offset().top - 50;
            anime_left = cart.offset().left;
            imgtodrag = prod_img.eq(0);
            img_top = imgtodrag.offset().top;
            img_left = imgtodrag.offset().left;
        }
        else if(popup_prod_img.length > 0){
            imgtodrag = popup_prod_img.eq(0);
            anime_top = cart.offset().top + 20;
            anime_left = cart.offset().left - 920;
            img_top = imgtodrag.offset().top - 10;
            img_left = imgtodrag.offset().left - 750;
        }
        else{
            prod_img = $(this).parent().parent().parent().find('.ian-product-card__image')
            anime_top = cart.offset().top - 20;
            anime_left = cart.offset().left - 80 ;
            imgtodrag = prod_img.eq(0);
            console.log('imgshkfhs', imgtodrag)
            img_top = imgtodrag.offset().top;
            img_left = imgtodrag.offset().left;
        }
        if (imgtodrag != undefined) {
            var imgclone = imgtodrag.clone()
                .offset({
                top: img_top,
                left: img_left
            }).css({
                'opacity': '0.5',
                    'position': 'absolute',
                    'height': '150px',
                    'width': '150px',
                    'z-index': '100'
            }).appendTo($('body'))
                .animate({
                'top': anime_top,
                    'left': anime_left,
                    'width': 75,
                    'height': 75
            }, 1000, 'easeInOutExpo');
            imgclone.animate({
                'width': 0,
                    'height': 0
            }, function () {
                $(this).detach()
            });
        }
    });
})

