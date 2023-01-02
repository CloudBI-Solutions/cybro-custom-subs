odoo.define("sh_pos_create_so.Models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");
    var DB = require("point_of_sale.DB");
    const { Gui } = require("point_of_sale.Gui");

    DB.include({
        init: function (options) {
            this._super(options);
            this.all_sale_orders = [];
            this.order_uid = 0;
        },
        get_all_sale_orders: function () {
            return this.all_sale_orders;
        },
        remove_all_sale_orders: function () {
            this.all_sale_orders = [];
        }
    });

    models.load_fields('res.partner',['property_payment_term_id', 'property_supplier_payment_term_id','sh_customer_discount', 'sh_enable_max_dic', 'sh_maximum_discount', 'sh_discount_type','sh_own_customer', 'sh_user_point', 'sh_user_point_amount', 'sh_expiry_date', 'sh_loyalty_card_no', "not_allow_partial_payment", "lang", "mobile"])

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            _super_posmodel.initialize.call(this, session, attributes);
        },
        create_sale_order: function () {
            var self = this;
            return new Promise(function (resolve, reject) {
                try {
                    if (self.env.pos.db.get_all_sale_orders().length > 0) {
                        self.rpc({
                            // model: "sale.order",
                            model: "pos.config",
                            method: "pos_create_so",
                            args: [this, self.env.pos.db.get_all_sale_orders()],
                        }).then(function (orders) {
                            if(orders && orders.length <= 1){
                                Gui.showPopup('saleOrderPopup', {
                                    title: 'Sale Order',
                                    body: " Sale Order Created. ",
                                    orders: orders
                                })
                                                             
                            }else{
                                Gui.showPopup('saleOrderPopup', {
                                    title: 'Sale Order',
                                    body: " Sale Order Created. ",
                                })
                            }
                            self.db.remove_all_sale_orders();
                        }).catch(function (reason) {
                            Gui.showPopup('ErrorPopup', {
                                title: 'Offline',
                                body: 'When you online Sale order will be created automiatically.',
                            });
                            self.set_synch(self.get("failed") ? "error" : "disconnected", self.env.pos.db.get_all_sale_orders().length);
                        });
                    }
                } catch (error) {
                    self.set_synch(self.get("failed") ? "error" : "disconnected");
                }
            });
        }
    });

});
