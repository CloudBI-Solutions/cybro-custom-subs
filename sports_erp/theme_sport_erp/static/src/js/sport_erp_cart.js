odoo.define('theme_sport_erp.cart_set', function (require) {
"use strict";

var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
var Session = require('web.session');
var rpc = require('web.rpc');

publicWidget.registry.Import = publicWidget.Widget.extend({
    selector: '.oe_website_order',
    events: {
    'click .return-cart': '_onClickAddToCart',
    },

    _onClickAddToCart: function (event) {
        if (this.$el.find("input")[0]){
        var div = this.$el.find("input")[0].defaultValue;
        ajax.jsonRpc('/sport_erp_cart', 'call', {
                    'product_id': div,
                }).then(function(data){
                window.location.href = data;
                });
                }
    },
    });
    });