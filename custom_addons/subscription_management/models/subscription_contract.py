# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _


class subscription_contract(models.Model):
    _name = "subscription.contract"
    _inherit = 'mail.thread'
    _description = "Subscription Contract"
    _order = 'id desc'

    name = fields.Char(string='Name', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related="company_id.currency_id",
                                  required=True, readonly=False,
                                  string='Currency')
    freeze_period = fields.Integer(string="Freeze period", default=30,
                                   copy=False, store=True)
    freeze_price = fields.Monetary(string="Freeze Price", copy=False,
                                   store=True)
    allowed_freeze_count = fields.Integer(string="Allowed Freeze Count",
                                          default=0)
    partner_id = fields.Many2one('res.partner', string="Customer Name")
    payment_date = fields.Selection([('5', '5th'), ('15', '15th'), ('25', '25th')],
                                    default='5', string='Payment Date', track_visibility="always", copy=False,
                                    required=True)
    contract_status = fields.Selection([('active', 'Active'), ('finished', 'Finished'), ('yet_start', 'Yet to start')],
                                       default='active', string='Contract Status', track_visibility="always",
                                       copy=False)
    reason = fields.Selection([('new_member', 'New Member'), ('renewal', 'Renewal'), ('new_site', 'New Site Move')],
                              default='new_member', string='Reason', track_visibility="always", copy=False)
    description = fields.Text(string='Notes', translate=True)
    signed_agreement = fields.Binary(string="Signed Agreement")
    signed_agreement_name = fields.Char(string="Signed Agreement Name")
    latest_record = fields.Boolean(string="Latest Record", default=False)
    contract_type = fields.Selection([('online', 'Online'), ('studio', 'Studio')], default='online',
                                     string='Contract Type', track_visibility="always", copy=False)
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', check_company=True,  # Unrequired company
        required=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", tracking=1,
        help="If you change the pricelist, only newly added lines will be affected.")
    subscription_ids = fields.One2many('subscription.subscription', 'contract_id', string="Subscriptions")


class SubscriptionFreeze(models.Model):
    _name = "subscription.freeze"
    _inherit = 'mail.thread'
    _description = "Subscription Freeze"
    _order = 'id desc'

    currency_id = fields.Many2one('res.currency', string='Currency', store=True)
    subscription_id = fields.Many2one('subscription.subscription', string="Subscription", required=True)
    start_date = fields.Date(string="Start Date", default=fields.Date.context_today, required=True)
    end_date = fields.Date(string="End Date", required=True)
    order_status = fields.Selection([('active', 'Active'), ('finished', 'Finished')], default='active',
                                    string='Order Status', track_visibility="always", copy=False)

    # @api.model
    # def create(self, vals):
    #     freeze = super(SubscriptionFreeze, self).create(vals)
    #     if vals.get('start_date') and vals.get('end_date'):
    #         fmt = '%Y-%m-%d'
    #         d1 = datetime.strptime(vals.get('start_date'), fmt)
    #         d2 = datetime.strptime(vals.get('end_date'), fmt)
    #         freeze_days = int((d2 - d1).days)
    #         print(freeze_days)
    #         print(vals['subscription_id'])
    #         subscription = self.env['subscription.subscription'].browse(vals['subscription_id'])
    #         print(type(subscription.frozen_days), type(freeze_days))
    #         print(subscription.frozen_days, freeze_days)
    #         subscription.frozen_days = subscription.frozen_days + freeze_days
    #
    #         query = 'SELECT * FROM public.product_warranty_warranty'
    #
    #     return freeze

    # @api.onchange('product_id')
    # def on_change_product(self):
    #     for current_rec in self:
    #         product = current_rec.product_id
    #         customer = current_rec.subscription_id.customer_name
    #         uom = current_rec.product_id.product_tmpl_id.uom_id.id
    #         price_list = current_rec.subscription_id.contract_id.pricelist_id
    #
    #         print('product', product, 'customer', customer, 'price_list', price_list)
    #
    #         if current_rec.product_id:
    #             current_rec.price = price_list.get_product_price(
    #             product, current_rec.quantity, customer, self.start_date, uom)
    #             current_rec.total = current_rec.price
    #         current_rec.end_date = fields.Date.add(current_rec.start_date,
    #                                                months=self.product_id.freeze_months * current_rec.quantity)

    # @api.onchange('discount')
    # def on_change_discount(self):
    #     for current_rec in self:
    #         print(self.subscription_id)
    #         current_rec.total = (current_rec.price * current_rec.quantity) - current_rec.discount
    #
    # @api.onchange('quantity')
    # def on_change_quantity(self):
    #     for current_rec in self:
    #         current_rec.total = current_rec.price * current_rec.quantity - current_rec.discount
    #         current_rec.end_date = fields.Date.add(current_rec.start_date,
    #                                                months=self.product_id.freeze_months * current_rec.quantity)

    @api.onchange('start_date')
    def on_change_start_date(self):
        for current_rec in self:
            current_rec.end_date = fields.Date.add(current_rec.start_date,
                                                   months=self.product_id.freeze_months * current_rec.quantity)
