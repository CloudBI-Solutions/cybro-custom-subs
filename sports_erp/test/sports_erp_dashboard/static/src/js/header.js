odoo.define('sports_erp_dashboard.header', function (require) {
    "use strict";
     $(document).ready(function () {
        let backGround = document.querySelector('.set-dashboard__menu-overlay');
        console.log(backGround);
        $('.set-dashboard__menu-overlay').click(function(ev) {
            console.log("clicked");
        });

     });
});