odoo.define('iwesabe_website_theme.cart', function (require) {

	var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc')
    var wSaleUtils = require('website_sale.utils');

//    var CartQuantity = require('sale.variant_mixin')


    publicWidget.registry.infiniarc_cart = publicWidget.Widget.extend({
        selector: '.wrapwrap',
        read_events: {
            'click  .js_delete_product': '_onClickDeleteProduct',
            'change .js_quantity': '_onChangeQuantity',
            'click .show_coupon': '_onClickShowCoupon'
//            'click a.js_add_cart_json': '_onClickAddCartJSON',
        },
        init: function () {
            this._super.apply(this, arguments);
        },


    _onClickShowCoupon: function (ev) {
        $(ev.currentTarget).hide();
        $('.coupon_form').removeClass('d-none');
    },
    _onClickDeleteProduct: function (ev) {
        ev.preventDefault();
        console.log('delete cart.................')
        $(ev.currentTarget).closest('tr').find('.js_quantity').val(0).trigger('change');
        window.location.reload();
    },

    _onChangeQuantity: function(ev) {
        console.log("Changing quantitiess........1")
        ev.preventDefault();
        let self = this,
            $target = $(ev.currentTarget),
            quantity = parseInt($target.val());

        this._callUpdateLineRoute(self.orderDetail.orderId, {
            'line_id': $target.data('lineId'),
            'input_quantity': quantity >= 0 ? quantity : false,
            'access_token': self.orderDetail.token
        }).then((data) => {
            self._updateOrderLineValues($target.closest('tr'), data);
            self._updateOrderValues(data);
        });
    },

        _onUpdateQuantity: function(ev){
            /* Update the cart quantity and price while change the product quantity from input */
//            ev.preventDefault();
            var $link = $(ev.currentTarget);
            var $input = $link.closest('.input-group').find("input");
            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            var previousQty = parseFloat($input.val() || 0, 10);
            var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
            var newQty = quantity > min ? (quantity < max ? quantity : max) : min;

            if (newQty !== previousQty) {
                $input.val(newQty).trigger('change');
            }
            return false;
        },
        _onChangeQuantity: function (ev){
            /* Get the updated data while change the cart quantity from cart. */
            var $input = $(ev.currentTarget);
            var self = this;
            $input.data('update_change', false);
            var value = parseInt($input.val() || 0, 10);
            if (isNaN(value)) {
                value = 1;
            }
            var line_id = parseInt($input.data('line-id'), 10);
            rpc.query({
                route: "/shop/cart/update_json",
                params: {
                    line_id: line_id,
                    product_id: parseInt($input.data('product-id'), 10),
                    set_qty: value
                },
            }).then(function (data) {
                $input.data('update_change', false);
                console.log('ssssssssssssrrrrrrrrrrrrrr')
                var check_value = parseInt($input.val() || 0, 10);
                if (isNaN(check_value)) {
                    check_value = 1;
                }
                if (value !== check_value) {
                    $input.trigger('change');
                    return;
                }
                if (!data.cart_quantity) {
                    return window.location = '/shop/cart';
                }
                wSaleUtils.updateCartNavBar(data);
                $input.val(data.quantity);
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
                $(".popover-header").html(data.quantity);
                $.get("/shop/cart", {
                    type: 'popover',
                }).then(function(data) {
                    $(".mycart-popover .popover-body").html(data);
                    $('.mycart-popover .js_add_cart_json').off('click').on('click',function(ev) {
//                        ev.preventDefault();
                        self._onUpdateQuantity(ev)
                    });
                    $(".mycart-popover .js_quantity[data-product-id]").off('change').on('change',function(ev) {
//                        ev.preventDefault();
                        self._onChangeQuantity(ev)
                    });
                    $(".mycart-popover .js_delete_product").off('click').on('click',function(ev) {
//                        ev.preventDefault();
                        self._onClickRemoveItem(ev)
                    });
                });
                window.location.reload();
            });
        }
    });
    $(document).ready(function(){
        $("#clear_cart_button").click(function(){
			ajax.jsonRpc("/shop/clear_cart", "call", {}).then(function() {
                    window.location.reload();
                });
                location.reload();
		});
    });
    $('#wrapwrap').scroll(() => {
        try{
               var tr_count = 0;
               $('#cart-products-table > tbody  > tr').each(function(){
                    tr_count += 1;
               });
              if(tr_count > 4){
                  var topOfFooter = $('#footer').position().top;
                  var scrollDistanceFromTopOfDoc = $(document).scrollTop() + 700;
                  var scrollDistanceFromTopOfFooter = scrollDistanceFromTopOfDoc - topOfFooter;
                  if (scrollDistanceFromTopOfDoc > topOfFooter && $(document).width() > 888) {
                    $('.cart_calculations').css('margin-top',  0 - scrollDistanceFromTopOfFooter);
                  } else  {
                    $('.cart_calculations').css('margin-top', 0);
                  }
              }
              else{
                $('.cart_calculations').css('position', 'inherit');
              }
        }
        catch{}
    });


//    function _onClickRemoveItem(ev) {
//            /* Remove the cart product while click on the remove product icon from cart */
//            $(ev.currentTarget).parent().siblings().find('.js_quantity').val(0).trigger('change');
//        };
//
//    $(document).ready(function(ev){
//            $(".js_delete_product").click(function(){
//                console.log('deleting...............')
//                console.log('eeevvvvvvvv', ev)
//                console.log('thisssss', this)
//                console.log('wwww', $(ev.currentTarget))
//                $(ev.currentTarget).parent().siblings().find('.js_quantity').val(0).trigger('change');
////                ev.preventDefault();
////                this._onClickRemoveItem(ev)
//                    });
//            });


	$(document).ready(function() {
		$(".js-fa-minus").click(function(){
			var product_id = $(this).attr('product-id');
//			location.reload(true);
		});

		function formatted_url(r){
			var a={search:{},hash:{}},
				e=new URL(r);
			for(var s of Array(2).keys())
				for(var n=1==s?"hash":"search",h=e[n].substring(1).split("&"),t=0;t<h.length; t++){
					var o=h[t].split("=");
					o[0]&&(a[n][o[0]] = decodeURIComponent(o[1]))
				}
			return a
		}
		
		function url_to_string(obj) {
			var str = [];
			for(var p in obj)
				str.push(encodeURIComponent(p) + "=" + obj[p]);
			return `?${str.join("&")}`;
		}

		$(".widget-content .search-attribute").on('keyup',function(e){
			if (e.which == 13){
				var search_query = $(this).val();
				var url_query = formatted_url(location.href);
				if (search_query){
					url_query.search.q = search_query;
				}
				else{
					delete url_query.search.q;
				}
				var new_query = url_to_string(url_query.search);
				$.post("/get_gear_store_type_view", url_query.search, function( data ) {
					$("#product-view-list").html( data );
				});
				history.pushState(null, null, new_query);
			}
		})

		function price_page_load(e){
			var min_price = parseInt($(".min-price").val());
			var max_price = parseInt($(".mix-price").val());
			var price_change_warning = $(".price_change_warning");
			price_change_warning.addClass('d-none');
			var price_query = '';
			if (min_price && max_price){
				if (min_price > max_price){
					price_change_warning.removeClass('d-none');
				}
				else {
					price_query = `${min_price}-${max_price}`
				}
			}
			else if (min_price){
				price_query = `${min_price}-`
			}
			else if (max_price){
				price_query = `-${max_price}`
			}
			else {
				price_query = ''
			}
			var url_query = formatted_url(location.href);
			if (price_query){
				url_query.search.price = price_query;
			}
			else {
				delete url_query.search.price;
			}
			var new_query = url_to_string(url_query.search);
			console.log ("new_query-=============",new_query)
			console.log ("url_query.search====----",url_query.search)
			$.post("/get_gear_store_type_view", url_query.search, function( data ) {
				$("#product-view-list").html( data );
			});
			history.pushState(null, null, new_query);
		}

		$(".min-price").on('focusout',price_page_load)
		$(".mix-price").on('focusout',price_page_load)

		$(".attr-brand").click(function(){
			var attr_brand_input = $(".attr-brand-input");
			var branch_ids = [];
			for (var i=0;i<attr_brand_input.length;i++){
				if ($(attr_brand_input[i]).prop("checked")){
					branch_ids.push($(attr_brand_input[i]).attr("filter-data"))
				}
			}
			var branch_query = branch_ids.join("-");
			var url_query = formatted_url(location.href);
			if (branch_query){
				url_query.search.brands = branch_query;
			}else{
				delete url_query.search.brands;
			}
			var new_query = url_to_string(url_query.search);
			console.log("new_query=----------",new_query)
			$.post("/get_gear_store_type_view", url_query.search, function( data ) {
				$("#product-view-list").html( data );
			});
			history.pushState(null, null, new_query);
		});

//		$(".attr-brand").click(function(){
//			var url = $(this).attr('url');
//			var data_id = $(this).attr('filter-data');
//			$.post("/get_gear_store_type_view", {'brands': data_id}, function( data ) {
//				$("#product-view-list").html( data );
//			});
//			history.pushState(null, null, "?brands="+data_id);
//		});
		
	});
});

odoo.define('iwesabe_website_theme.index', function(require) {
    $(document).on("click", "#otp_logout_page", function() {
    var close= $("#login_popup")
    close.trigger('click');

    });
    $(document).on("click", "#o_logout_again", function() {
     var close_popup= $("#otp_login")
     close_popup.trigger('click');
    });
     $(document).on("click", "#get_otp_logout_page", function() {
     var close_otp_popup= $(".otp")
     close_otp_popup.trigger('click');
     });
//     $(document).on("click", "#login_btn", function() {
//     console.log("ggggggg")
//     }

    })