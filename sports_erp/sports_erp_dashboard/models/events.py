from odoo import fields, models


class Events(models.Model):
    _inherit = "event.event"

    organisation_ids = fields.Many2many('organisation.organisation')
    is_able_to_assign = fields.Boolean('Is Able to Assign')

