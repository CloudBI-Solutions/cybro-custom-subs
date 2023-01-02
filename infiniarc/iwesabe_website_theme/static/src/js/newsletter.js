odoo.define('iwesabe_website_theme.subscribe_newsletter', function (require) {
    "use strict";
     var ajax = require('web.ajax');

    $(document).ready(function() {

        $(".ian_newsletter_subscribe").click(function(e){
            var email = $(this).parent().find('.email-subscriber').val()
            if (!email.match(/.+@.+/)) {
                $(this).parent().find('.form-control').addClass('is-invalid');
                return false;
            }else{
                $(this).parent().find('.form-control').removeClass('is-invalid');
                        ajax.jsonRpc("/ian/newsletter/subscribe", "call", {'email': email})
                .then(function() {

                });
            }

        })
    })
})