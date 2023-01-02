odoo.define('product_branding.receipt', function(require){
    "use strict";
    var models = require('point_of_sale.models');
    models.load_fields('product.product', ['brand_name']);
    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function(){
            var line = _super_orderline.export_for_printing.apply(this, arguments);
            line.brand_name = this.get_product().brand_name;
//            console.log('brand_name = ',line.brand_name)
            return line;
        },
    });
});