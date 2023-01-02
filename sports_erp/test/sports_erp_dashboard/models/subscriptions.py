from odoo import fields, models


class SubscriptionSubscription(models.Model):
    _inherit = "subscription.subscription"

    organisation_ids = fields.Many2many('organisation.organisation',
                                        'subscription_organisation_rel',
                                        'sub_id', 'org_id',
                                        string="Organisations")
    is_able_to_assign = fields.Boolean('Is Able to Assign')
    customer_ids = fields.Many2many('res.partner', 'subscription_partner_rel')


class SubscriptionPlan(models.Model):
    _inherit = "subscription.plan"

    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 index=True,
                                 default=lambda self: self.env.company)
    organisation_ids = fields.Many2many('organisation.organisation',
                                        'plan_organisation_rel',
                                        'plan_id', 'org_id',
                                        string="Organisations")


class SubscriptionContract(models.Model):
    _inherit = "subscription.contract"

    company_id = fields.Many2one('res.company', 'Company',
                                 required=True,
                                 index=True,
                                 default=lambda self: self.env.company)
    organisation_ids = fields.Many2many('organisation.organisation',
                                        'contract_organisation_rel',
                                        'contract_id', 'org_id',
                                        string="Organisations")
    customer_ids = fields.Many2many('res.partner', 'subscription_contract_partner_rel')


class SubscriptionReasons(models.Model):
    _inherit = "subscription.reasons"

    company_id = fields.Many2one('res.company', 'Company',
                                 required=True,
                                 index=True,
                                 default=lambda self: self.env.company)
    organisation_ids = fields.Many2many('organisation.organisation',
                                        'reason_organisation_rel',
                                        'reason_id', 'org_id',
                                        string="Organisations")

class SubscriptionProduct(models.Model):
    _inherit = 'product.template'

    organisation_ids = fields.Many2many('organisation.organisation',
                                        'product_organisation_rel',
                                        'product_id', 'org_id',
                                        string="Organisations")
    is_able_to_assign = fields.Boolean('Is Able to Assign')
