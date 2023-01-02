odoo.define('product_branding.brand_name', function(require){
    'use strict';
    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;

//    console.log("models hi",models)
    models.load_fields('product.product',['brand_name']);
    models.Orderline = models.Orderline.extend({
        initialize: function(attr,options){
            var line = _super_orderline.initialize.apply(this,arguments);
            this.brand_name = this.get_product().brand_name;
//            console.log("brand name = ",this.brand_name)
        }
    });
});
