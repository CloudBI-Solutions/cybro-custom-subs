from odoo import api, fields, models
import datetime
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    subscription_contract_id = fields.Many2one('subscription.contract',
                                               string='Subscription Contract')

    @api.onchange('subscription_contract_id')
    def on_change_subscription_contract(self):
        for current_rec in self:
            current_rec.order_line = None
            subscriptions = \
                current_rec.subscription_contract_id.subscription_ids
            current_rec.partner_id = \
                current_rec.subscription_contract_id.partner_id
            for subscription in subscriptions:
                self.write({'order_line': [[0, 0, {
                    'product_id': subscription.product_id,
                    'order_id': self.id,
                    'product_uom': subscription.product_id.uom_id,
                    'name': '[' + subscription.product_id.default_code + ']' +
                           subscription.product_id.name, 'subscribed': True}]]})

                # product_list = []
                # for record in self.invoice_id.invoice_line_ids.product_id:
                #     product_list.append(record.id)
                # return {'domain': {'product_id': [('id', 'in', product_list)]}}

    def action_subscribe(self):
        for record in self:
            for rec in record.order_line:
                if not rec.subscribed:
                    if rec.product_id.activate_subscription:
                        start_date = datetime.today().date()
                        rec.subscribed = True
                        subscription = record.env[
                            'subscription.subscription'].create(
                            {
                                'contract_id':
                                rec.product_id.subscription_contract_id,
                                'product_id': rec.product_id.id,
                                'price': rec.product_id.list_price,
                                'quantity': rec.product_uom_qty,
                                'customer_name': record.partner_id.id,
                                'active': True,
                                'start_date': start_date,
                                'num_billing_cycle':
                                rec.product_id.subscription_plan_id.num_billing_cycle,
                                'sub_plan_id':
                                rec.product_id.subscription_plan_id.id,
                                'duration':
                                rec.product_id.subscription_plan_id.duration,
                                'unit': rec.product_id.subscription_plan_id.unit,
                                'source': 'so',
                                'so_origin': record.id,
                            })


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    subscribed = fields.Boolean(string='Subscribed', default=False)
