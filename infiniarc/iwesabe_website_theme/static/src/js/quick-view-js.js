odoo.define('iwesabe_website_theme.quick_view_js', function(require) {
    'use strict';

    var sAnimations = require('website.content.snippets.animation');
    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var WebsiteSale = publicWidget.registry.WebsiteSale;
//    var productDetail = new publicWidget.registry.productDetail();
    var core = require('web.core');
    var QWeb = core.qweb;
    var xml_load = ajax.loadXML(
        '/website_sale_stock/static/src/xml/website_sale_stock_product_availability.xml',
        QWeb
    );

//$(document).on("click", ".o_add_wishlist", function () {
////    var ajax = require('web.ajax');
//     var wishlist_id = $(this).data('id');
//     ajax.jsonRpc('/shop/wishlist/add', 'call', {'product_id':wishlist_id
//
//                    }).then(function (data) {
//                        if(data){
//
//                            $('#infiniarc-wishlist').html(data);
//                        }
//
//                    });
//});


$(document).on("click", ".button_modal_info", function () {
//    var ajax = require('web.ajax');
     var myBookId = $(this).data('id');
     console.log('myBookId', myBookId)
     ajax.jsonRpc('/quick/model', 'call', {'id':myBookId

                    }).then(function (data) {
                        console.log('dasa....', data)
                        if(data){
                            $('#dialogue_data_quick_view').html(data);
                        }

                    });

});

$(document).on("click", ".button_gear_info", function () {
//    var ajax = require('web.ajax');
     var myBookId = $(this).data('id');
     ajax.jsonRpc('/gear/model', 'call', {'id':myBookId

                    }).then(function (data) {
                        if(data){
                            $('#dialogue_data_type_view').html(data);
                        }

                    });
});

$(document).on("click", ".button_micro_info", function () {
//    var ajax = require('web.ajax');
    console.log('button_micro_info....')
     var myBookId = $(this).data('id');
     console.log('myBookId', myBookId)
     ajax.jsonRpc('/microdynamic', 'call', {'id':myBookId

                    }).then(function (data) {
                        console.log('datasssssss', data)
                        if(data){
                            $('#dialogue_micro_type_view').html(data);
                        }

                    });
});

$(document).on("click", ".button_pc_info", function () {
//    var ajax = require('web.ajax');
     var myBookId = $(this).data('id');
     ajax.jsonRpc('/gear/model', 'call', {'id':myBookId

                    }).then(function (data) {
                        if(data){
                            $('#dialogue_pc_type_view').html(data);
                        }

                    });
});

$(document).on("click", ".button_modal_special_info", function () {
//    var ajax = require('web.ajax');
     var myBookId = $(this).data('id');
     ajax.jsonRpc('/special/model', 'call', {'id':myBookId

                    }).then(function (data) {
                        if(data){

                            $('#dialogue_data_special_view').html(data);
                        }

                    });
});

$(document).on("click", ".button_product_spec", function () {
//    var ajax = require('web.ajax');
     var myBookId = $(this).data('id');
     ajax.jsonRpc('/product/spec_model', 'call', {'id':myBookId

                    }).then(function (data) {
                        if(data){

                            $('#dialogue_product_spec_view').html(data);
                        }

                    });
});


    publicWidget.registry.quickView = publicWidget.Widget.extend({
        selector: ".wrap_product",
        events: {
//            'show.bs.modal': '_onShowModal',
            'click #quick_view_button': 'initQuickView',
        },

        initQuickView(ev) {
//            ev.preventDefault()
            self = this;
//            var ajax = require('web.ajax');
//            var element = ev.currentTarget;
            var myBookId = $(this).data('id');
            ajax.jsonRpc('/quick/model', 'call', {'id':myBookId}).then(function(data) {

                var header = '<h4>'+ data.name +'</h4>'
                var description = '<p>'+ data.details +'</p>'
                var new_price = '<span>'+ data.offer +'</span>'
                var old_price = '<span>'+ data.std +'</span>'
                var image = `<img src="/web/image/product.template/${data['id']}/image_1920" class="item-slick"/>`
//                        var image = '<img src="/web/image/product.template/${data.id}/image" class="item-slick"/>'
                document.getElementById('quick_view_header').innerHTML = header
                document.getElementById('quick_view_description').innerHTML = description
                document.getElementById('new_price').innerHTML = new_price
                document.getElementById('old_price').innerHTML = old_price
                document.getElementById('view_img').innerHTML = image
            });

        },
        _onShowModal(ev){
                console.log('jklljjjjjjjjjjjjjjjjjjjjj')
                ev.preventDefault()
            self = this;
            var ajax = require('web.ajax');
            var element = ev.currentTarget;
            var myBookId = $(this).data('id');
            console.log('myBookId',$(this).data())
//            var product_id = $(element).attr('data-id');
            ajax.jsonRpc('/quick/model', 'call', {'id':myBookId}).then(function(data) {

                console.log('data', data)
                var header = '<h4>'+ data.name +'</h4>'
                var description = '<p>'+data.details+'</p>'
                var new_price = '<span>'+data.offer+'</span>'
                var old_price = '<span>'+data.std+'</span>'
                console.log('data.........', data)
                var image = `<img src="/web/image/product.template/${data['id']}/image_1920" class="item-slick"/>`
//                        var image = '<img src="/web/image/product.template/${data.id}/image" class="item-slick"/>'
                document.getElementById('quick_view_header').innerHTML = header
                document.getElementById('quick_view_description').innerHTML = description
                document.getElementById('new_price').innerHTML = new_price
                document.getElementById('old_price').innerHTML = old_price
                document.getElementById('view_img').innerHTML = image

            });

        },
    });
    $('#quick_view_model_shop').on('hidden.bs.modal', function (e) {
        $("#quick_view_model_shop .modal-body").html('');
        $("#quick_view_model_shop .modal-header .modal-title").text('');
    });
});