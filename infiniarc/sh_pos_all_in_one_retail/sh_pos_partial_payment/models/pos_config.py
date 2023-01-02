# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api
from odoo.tools import float_is_zero, float_round, float_repr, float_compare

class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_partial_payment = fields.Boolean("Allow Partial Payment")
    sh_allow_to_pay_order = fields.Boolean(string="Allow To Pay Order")

    sh_partial_pay_product_id = fields.Many2one('product.product', string="Partial Pay Product")


    @api.onchange('sh_allow_to_pay_order')
    def _onchange_sh_allow_to_pay_order(self):
        if self.sh_allow_to_pay_order:
            product = self.env['product.product'].sudo().search([('sh_is_partial_pay_product', '=', True)], limit=1)
            if product:
                self.sh_partial_pay_product_id = product.id
            
class ResPartner(models.Model):
    _inherit = 'res.partner'

    not_allow_partial_payment = fields.Boolean("Not Allow Partial Payment")

class PosOrder(models.Model):
    _inherit = 'pos.order'

    sh_amount_residual = fields.Monetary(string='Amount Due', 
        compute='_compute_amount')

    def action_pos_order_paid(self):
        self.ensure_one()

        # TODO: add support for mix of cash and non-cash payments when both cash_rounding and only_round_cash_method are True
        if not self.config_id.cash_rounding \
           or self.config_id.only_round_cash_method \
           and not any(p.payment_method_id.is_cash_count for p in self.payment_ids):
            total = self.amount_total
        else:
            total = float_round(self.amount_total, precision_rounding=self.config_id.rounding_method.rounding, rounding_method=self.config_id.rounding_method.rounding_method)

        isPaid = float_is_zero(total - self.amount_paid, precision_rounding=self.currency_id.rounding)
        if self and self.state == 'on_hold':
            if not isPaid and not self.config_id.cash_rounding:
                raise UserError(_("Order %s is not fully paid.", self.name))
            elif not isPaid and self.config_id.cash_rounding:
                currency = self.currency_id
                if self.config_id.rounding_method.rounding_method == "HALF-UP":
                    maxDiff = currency.round(self.config_id.rounding_method.rounding / 2)
                else:
                    maxDiff = currency.round(self.config_id.rounding_method.rounding)
            
                diff = currency.round(self.amount_total - self.amount_paid)
                if not abs(diff) <= maxDiff:
                    raise UserError(_("Order %s is not fully paid.", self.name))
        self.write({'state': 'paid'})

        return True

    def _compute_amount(self):
        for each in self:
            if each.amount_paid < each.amount_total:
                each.sh_amount_residual = each.amount_total-each.amount_paid
            else:
                each.sh_amount_residual = 0.00

    @api.model
    def _process_order(self, order, draft, existing_order):
        order_id = super(PosOrder, self)._process_order(
            order, draft, existing_order)
        if order_id:
            order_obj = self.env['pos.order'].search([('id','=',order_id)])
            if order_obj and order_obj.to_invoice and not order_obj.account_move:
                order_obj.action_pos_order_invoice()

        return order_id

    @api.model
    def create_from_ui(self, orders, draft=False):
        existing_return_order = []
        for order in orders:
            existing_order = False
            if 'server_id' in order['data']:
                existing_order = self.env['pos.order'].search(['|', ('id', '=', order['data']['server_id']), ('pos_reference', '=', order['data']['name'])], limit=1)
                if existing_order:
                    existing_return_order.append({'id':existing_order.id,'pos_reference':existing_order.pos_reference})
                    pos_session = self.env['pos.session'].browse(order['data']['pos_session_id'])
                    old_payment_line = []
                    if existing_order.payment_ids :
                        for each_payment_line in existing_order.payment_ids:
                            old_payment_line.append([0, 0, {'name': each_payment_line.payment_date, 'payment_method_id': each_payment_line.payment_method_id.id, 'amount': each_payment_line.amount, 'payment_status': each_payment_line.payment_status, 'ticket': each_payment_line.ticket, 'card_type': each_payment_line.card_type, 'cardholder_name': each_payment_line.cardholder_name, 'transaction_id': each_payment_line.transaction_id}])
                    
                    self._process_payment_lines(order['data'], existing_order, pos_session, draft)

                    if existing_order and existing_order.to_invoice:
                        existing_order._apply_invoice_payments()

                    if old_payment_line and len(old_payment_line) > 0:
                            for each_old_payment_line in old_payment_line:
                                order['data']['statement_ids'].append(each_old_payment_line)
                    
                    self._process_payment_lines(order['data'], existing_order, pos_session, draft)
                    existing_order.action_pos_order_paid()
                    if existing_order and existing_order.to_invoice:
                        existing_order.write({'state':'invoiced'})

        order_id = super(PosOrder, self).create_from_ui(orders, draft=False)
        if existing_return_order and len(existing_return_order) > 0:
            for each_existing_return_order in existing_return_order:
                order_id.append(each_existing_return_order)
        return order_id

class ProductProduct(models.Model):
    _inherit = 'product.product'

    sh_is_partial_pay_product = fields.Boolean('Partial Pay Product')