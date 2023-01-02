from odoo import fields, models, api, _
from random import randint
from dateutil.relativedelta import relativedelta


class Subscription(models.Model):
    _inherit = "subscription.subscription"

    athlete_id = fields.Many2one('organisation.athletes', string="Athletes",
                                 compute='compute_athlete_id', store=True)
    parent_id = fields.Many2one('organisation.parents', string="Parents",
                                compute='compute_parent_id', store=True)
    coach_id = fields.Many2one('organisation.coaches', string="Coaches",
                               compute='compute_coach_id', store=True)

    @api.depends('customer_name')
    def compute_athlete_id(self):
        for rec in self:
            athletes_id = self.env['organisation.athletes'].search([
                ('partner_id', '=', rec.customer_name.id)], limit=1)
            print("Customer", athletes_id)
            rec.athlete_id = athletes_id if athletes_id else None

    @api.depends('customer_name')
    def compute_parent_id(self):
        for rec in self:
            parent_id = self.env['organisation.parents'].search([
                ('partner_id', '=', rec.customer_name.id)], limit=1)
            print("Customer", parent_id)
            rec.parent_id = parent_id if parent_id else None

    @api.depends('customer_name')
    def compute_coach_id(self):
        for rec in self:
            coach_id = self.env['organisation.coaches'].search([
                ('partner_id', '=', rec.customer_name.id)], limit=1)
            print("Customer", coach_id)
            rec.coach_id = coach_id if coach_id else None


class Athletes(models.Model):
    """model for managing athletes"""
    _inherit = "organisation.athletes"

    subscription_count = fields.Integer(compute='compute_subscription_count')
    subscription_ids = fields.One2many('subscription.subscription',
                                       'athlete_id', compute='_compute_subscription_ids'
                                       )

    @api.depends('partner_id')
    def _compute_subscription_ids(self):
        for athlete in self:
            subscriptions = self.env['subscription.subscription'].search(
                [('athlete_id', '=', athlete.id)])
            print(subscriptions.read(), "sub")
            athlete.subscription_ids = subscriptions

    def compute_subscription_count(self):
        for rec in self:
            rec.subscription_count = self.env[
                'subscription.subscription'].search_count([
                ('customer_name', '=', self.partner_id.id)])

    def action_subscription(self):
        return {
            'name': _('Subscriptions'),
            'view_mode': 'tree,form',
            'domain': [('customer_name', '=', self.partner_id.id)],
            'res_model': 'subscription.subscription',
            'type': 'ir.actions.act_window',
        }


