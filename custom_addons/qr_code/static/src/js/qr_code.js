odoo.define('qr_code.qr', function (require) {
   "use strict";
   console.log("haaaai")
   var core = require('web.core');
   var QWeb = core.qweb;
   var Widget = require('web.Widget');
   var SystrayMenu = require('web.SystrayMenu');
   var rpc = require('web.rpc');
   var _t = core._t;
   var qr = Widget.extend({
       template: 'qr_template',
       events: {
           "click #btn_clear": "f_clear",
       },
       f_clear: function() {
            $("#text_input").val("");
        },


   });
   SystrayMenu.Items.push(qr);
   return qr;
});