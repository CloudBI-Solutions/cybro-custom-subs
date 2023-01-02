odoo.define("sh_pos_partial_payment.pos", function (require) {
    "use strict";

    var models = require("point_of_sale.models");
    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const return_exchange_screens = require("sh_pos_order_return_exchange.screen");
    const orderlist_screens = return_exchange_screens.OrderListScreen
    
    // models.load_fields("res.partner", ["not_allow_partial_payment"]);

   const PartialPOSOrderListScreen = (orderlist_screens) =>
       class extends orderlist_screens {
           draft_order_filter(){
               var self = this;
               if($('.sh_not_paid_order_button')){
                    if($('.sh_not_paid_order_button').hasClass('highlight')){
                       $('.sh_not_paid_order_button').removeClass('highlight')
                       self.filter_by_draft_order = false;

                       var data = $.grep(self.env.pos.db.all_display_order, function (e) {
                           return e.sh_amount_residual == 0.00;
                       });

                       $(".sh_pagination").pagination("updateItems", Math.ceil(data.length / self.env.pos.config.sh_how_many_order_per_page));
                       $(".sh_pagination").pagination("selectPage", 1);

                    }else{
                        $('.sh_not_paid_order_button').addClass('highlight')
                        $('.sh_paid_order').removeClass('highlight')
                        $('.sh_posted_order').removeClass('highlight')
                        $('.sh_invoiced_order').removeClass('highlight')
                        self.filter_by_draft_order = true;
                        self.filter_by_paid_order = false;
                        self.filter_by_posted_order = false;
                        self.filter_by_invoice_order = false;
                        // var data = $.grep(self.env.pos.db.all_display_order, function (e) {
                        //    return e.sh_amount_residual > 0.00;
                        // });

                        // $(".sh_pagination").pagination("updateItems", Math.ceil(data.length / self.env.pos.config.sh_how_many_order_per_page));
                        $(".sh_pagination").pagination("selectPage", 1);
                    }
                    self.render();
                }
            } 
            pay_pos_order(event){
                var self = this;
                var order_id = $(event.currentTarget.closest("tr")).attr("data-order-id");
                if (order_id) {
                    var order_data = self.env.pos.db.order_by_uid[order_id];
                    if (!order_data) {
                        order_data = self.env.pos.db.order_by_id[order_id];
                    }
                    if(order_data){
                        if(order_data.sh_amount_residual > 0){
                            if(self.env.pos.get_order().get_orderlines().length > 0){
                                self.env.pos.add_new_order()
                            }
                            var current_order = self.env.pos.get_order()
                            var partial_product = self.env.pos.db.get_product_by_id(self.env.pos.config.sh_partial_pay_product_id[0])
                            if(current_order && partial_product){
                                current_order.is_due_paid = true
                                current_order.add_product(partial_product, {
                                    quantity: 1,
                                    price: order_data.sh_amount_residual,
                                });
                                if (order_data.partner_id && order_data.partner_id[0]) {
                                    current_order.set_client(self.env.pos.db.get_partner_by_id(order_data.partner_id[0]));
                                }
                                if(order_data && order_data.sh_amount_residual){
                                	current_order.sh_due_amount = order_data.amount_paid 
                                }else{
                                	current_order.sh_due_amount = 0.00
                                }
                                current_order.name = order_data.pos_reference;
                                current_order.to_invoice = order_data.to_invoice
                            }
                            self.trigger("close-temp-screen");
                            $(".pay").click();
                        }
                    }
                }
            }
        };
    Registries.Component.extend(orderlist_screens, PartialPOSOrderListScreen);

    // var _super_posmodel = models.PosModel.prototype;
    // models.PosModel = models.PosModel.extend({
    //     initialize: function (session, attributes) {
    //         var self = this;
    //         self.is_draft_filter = false;
    //         _super_posmodel.initialize.apply(this, arguments);
    //     },
    // });

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function () {
            var self = this;
            _super_Order.initialize.apply(this, arguments);
            self.is_due_paid = false;
            self.sh_due_amount = 0
            return this;
        },
        is_paid: function(){
            var self = this

            if(self.pos.config.enable_partial_payment && self.pos.get_order().to_invoice && self.pos.get_order().get_client() && !self.pos.get_order().get_client().not_allow_partial_payment){
                return true
            }else{
                return _super_Order.is_paid.apply(this, arguments);
            }
        },
        export_as_JSON: function () {
            var json = _super_Order.export_as_JSON.apply(this, arguments);
            json.is_due_paid = this.is_due_paid;
            return json;
        },
        export_for_printing: function () {
            var receipt = _super_Order.export_for_printing.apply(this, arguments);
            receipt['sh_due_amount'] = this.sh_due_amount;
            return receipt;
        },
    });

    const PosPartialPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            async validateOrder(isForceValidate) {
                var self = this;
                if(self.env.pos.config.enable_partial_payment && self.env.pos.get_order().to_invoice && self.env.pos.get_order().get_client() && self.env.pos.get_order().get_client().not_allow_partial_payment && !self.env.pos.get_order().is_paid()){
                    alert(self.env.pos.get_order().get_client().name + " is not allow to do partial payment.")
                }else if(self.env.pos.config.enable_partial_payment && !self.env.pos.get_order().to_invoice && self.env.pos.get_order().get_client() && !self.env.pos.get_order().get_client().not_allow_partial_payment && !self.env.pos.get_order().is_paid()){
                    alert("You can not do a partial payment without invoice.")
                }
                super.validateOrder(isForceValidate)
            }
        };

    Registries.Component.extend(PaymentScreen, PosPartialPaymentScreen);

});
