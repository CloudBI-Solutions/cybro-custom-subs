odoo.define('theme_sport_erp.header',function(require){
    "use strict";

    $(document).ready(function () {

       $('#mobileMenuToggler, #mobileMenuClose').on('click', function (e) {
       $('#mobileMenu').toggleClass('d-none');
        })

    });
});
