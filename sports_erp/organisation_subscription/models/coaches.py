from odoo import fields, models, api, _
from random import randint
from dateutil.relativedelta import relativedelta


class Coaches(models.Model):
    """model for managing athletes"""
    _inherit = "organisation.coaches"

    subscription_count = fields.Integer(compute='compute_subscription_count')
    subscription_ids = fields.One2many('subscription.subscription',
                                       'coach_id',
                                       compute='_compute_subscription_ids'
                                       )

    def compute_subscription_count(self):
        for rec in self:
            rec.subscription_count = self.env[
                'subscription.subscription'].search_count([
                ('customer_name', '=', self.partner_id.id)])

    @api.depends('partner_id')
    def _compute_subscription_ids(self):
        for coach in self:
            subscriptions = self.env['subscription.subscription'].search(
                [('coach_id', '=', coach.id)])
            print(subscriptions.read(), "sub")
            coach.subscription_ids = subscriptions

    def action_subscription(self):
        return {
            'name': _('Subscriptions'),
            'view_mode': 'tree,form',
            'domain': [('customer_name', '=', self.partner_id.id)],
            'res_model': 'subscription.subscription',
            'type': 'ir.actions.act_window',
        }
