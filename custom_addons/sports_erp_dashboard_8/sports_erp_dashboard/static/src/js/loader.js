odoo.define('sports_erp_dashboard.loader', function (require) {
    "use strict";
     $(document).ready(function () {
        var pathName = window.location.pathname;
        if (pathName == '/web/login'){
            document.getElementById('footer').style.display = 'none';
        }
        var el = document.getElementById(pathName);
        if (el){
            el.classList.add('set-dashboard__sidebar-link--active');
        }
     });
    });