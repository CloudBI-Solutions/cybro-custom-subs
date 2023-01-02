from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    last_name = fields.Char(string='Last Name')
