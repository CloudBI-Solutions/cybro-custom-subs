odoo.define('session_discount.session_discount', function(require){
    'use strict';

    var models = require('point_of_sale.models');
    var field_utils = require('web.field_utils');
    var core = require('web.core');
    const _t = core._t;
    const { Gui } = require('point_of_sale.Gui');
    var _super_orderline = models.Orderline.prototype;

    const DiscountButton = require('pos_discount.DiscountButton');
    const Registries = require('point_of_sale.Registries');

    var global_discount = 0;
    var discount_limit = 0;
    var total_line_discount = 0;
    var global_discount_amount = 0;
    var line_discount = 0;
    var pos_prod_id = [];
    var disc_calc = [];
    var i=0;
    var total_discount = 0;
    var flag = 0;

    models.Orderline = models.Orderline.extend({

    initialize: function(attr,options){
        var line = _super_orderline.initialize.apply(this,arguments);
        if(this.pos.config.limit_discount_check == true){
            discount_limit = this.pos.config.limit_discount;
            if (this.product.default_code != "DISC"){
                if (!pos_prod_id.includes(this.product.id)){
                    pos_prod_id.push(this.product.id)
                    disc_calc.push(0)
                    }
                console.log("product id", pos_prod_id)
                console.log("discount calc", disc_calc)
                }
            }
        },

    set_discount: function(discount){
        if (this.product.default_code != "DISC"){
            console.log("this.product", this.product.default_code)
            var prod_index = pos_prod_id.indexOf(this.product.id);
            console.log(prod_index)
            console.log(discount)
            disc_calc[prod_index] = (discount/100) * (this.quantity * this.price);
            console.log('disc_calc', disc_calc)
            total_line_discount = 0;
            for (i = 0; i < disc_calc.length; i++){
            total_line_discount += disc_calc[i];
                }
            console.log("disc_limit", discount_limit)
            console.log("total_line_discount", total_line_discount)
            total_discount = total_line_discount + global_discount_amount;
            console.log("total", total_discount)
            var parsed_discount = typeof(discount) === 'number' ? discount : isNaN(parseFloat(discount)) ? 0 : field_utils.parse.float('' + discount);
            var disc = Math.min(Math.max(parsed_discount || 0, 0),100);
            this.discount = disc;
            this.discountStr = '' + disc;
            this.trigger('change',this);

            if(total_discount > discount_limit){
                Gui.showPopup("ErrorPopup", {
                    'title': _t("Discount Not Possible"),
                    'body':  _t("You cannot apply discount above the discount limit."),
                    })
                    var order = this.pos.get_order();
                    console.log("here order", order)
                    order.get_selected_orderline().set_discount(0);
                }
            }
        },
    });


    const NewDiscountButton = DiscountButton =>
        class extends DiscountButton {

            async apply_discount(pc){
                var order = this.env.pos.get_order();
                var base_to_discount = order.get_total_without_tax();
                global_discount = - pc / 100.0 * base_to_discount;
                global_discount_amount = Math.abs(global_discount);
                console.log("global", global_discount_amount);
                total_discount = total_line_discount + global_discount_amount;
                console.log("total", total_discount)
                if(total_discount > discount_limit){
                    Gui.showPopup("ErrorPopup", {
                    'title': _t("Discount Not Possible"),
                    'body':  _t("You cannot apply discount above the discount limit."),
                        })
                    global_discount_amount = 0;
                    }
                else{
                    await super.apply_discount(pc);
                }
            }
        }
        DiscountButton.template = 'DiscountButton';
        Registries.Component.extend(DiscountButton, NewDiscountButton);

        return NewDiscountButton;

});
