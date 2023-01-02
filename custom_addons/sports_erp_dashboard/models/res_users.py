from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    organisation_ids = fields.Many2many('organisation.organisation')
