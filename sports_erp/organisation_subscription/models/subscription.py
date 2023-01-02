from odoo import fields, models, api, _


class Subscription(models.Model):
    _inherit = "subscription.subscription"

    organisation_id = fields.Many2one('organisation.organisation')


class SubscriptionContract(models.Model):
    _inherit = "subscription.contract"

    organisation_id = fields.Many2one('organisation.organisation')


class SubscriptionPlan(models.Model):
    _inherit = "subscription.plan"

    organisation_id = fields.Many2one('organisation.organisation')

