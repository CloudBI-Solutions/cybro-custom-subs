odoo.define('paceflow.upload_video', function(require){
    "use strict";
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    $(document).ready(function () {
      $('.paceflow-select').select2();
    });
    const dateEl = document.querySelector('.paceflow-datepicker');
//    if (dateEl){
//    const datepicker = new Datepicker(dateEl, {
//      autohide: true,
//      todayHighlight: true,
//      prevArrow: '<i class="fa fa-long-arrow-left" aria-hidden="true"></i>',
//      nextArrow: '<i class="fa fa-long-arrow-right" aria-hidden="true"></i>'
//            });
//        }
});