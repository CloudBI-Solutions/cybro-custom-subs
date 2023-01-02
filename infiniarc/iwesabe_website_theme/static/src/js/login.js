//odoo.define('iwesabe_website_theme.login', function(require) {
//    'use strict';
//
//    console.log('loginnnnnnn')
//    var searchOpen = document.querySelector('#openSearch');
//    var searchClose = document.querySelector('#closeSearch');
//    var searchDialog = document.querySelector('.ian-header__search');
//    var searchInput = document.querySelector('.ian-header__search-input');
//
//    // Open Search Dialog
//    searchOpen.addEventListener('click', function (e) {
//      e.preventDefault();
//      searchDialog.classList.toggle('d-none');
//      searchInput.focus();
//    }),
//    // Close Search Dialog
//    searchClose.addEventListener('click', function (e) {
//      e.preventDefault();
//      searchDialog.classList.toggle('d-none');
//    }),
//
//    var supportToggle = document.querySelector('#openSupport');
//    var supportModal = document.querySelector('.ian-header__support-detail');
//
//    supportToggle.addEventListener('click', function (e) {
//    supportModal.classList.toggle('d-none');
//    }),
//
//    var mobileToggler = document.querySelector('#menuToggle');
//    var mobileMenu = document.querySelector('.ian-header__nav');
//
//    mobileToggler.addEventListener('click', function (e) {
//    e.preventDefault();
//    mobileMenu.classList.toggle('ian-header__nav-hide');
//    mobileToggler.classList.toggle('is-active')
//    }),
//    });
//
////$(document).on("click", ".button_modal_info", function () {
////     var myBookId = $(this).data('id');
////     console.log($(this).data());
////    ajax.jsonRpc('/quick/model', 'call', {'id':myBookId
////
////                    }).then(function (data) {
////                        console.log('data', data)
////                        var header = '<h4>'+ data.name +'</h4>'
////                        var description = '<p>'+data.details+'</P>'
////                        var new_price = '<span>'+data.offer+'</span>'
////                        var old_price = '<span>'+data.std+'</span>'
////                        console.log('data.........', data)
////                        var image = `<img src="/web/image/product.template/${data['id']}/image_1920" class="card__image"/>`
//////                        var image = '<img src="/web/image/product.template/${data.id}/image" class="item-slick"/>'
////                        document.getElementById('quick_view_header').innerHTML = header
////                        document.getElementById('quick_view_description').innerHTML = description
////                        document.getElementById('new_price').innerHTML = new_price
////                        document.getElementById('old_price').innerHTML = old_price
////                        document.getElementById('view_img').innerHTML = image
////
////                    });
//
////     $(".modal-body .wrapper<h4>").val( myBookId );
//});