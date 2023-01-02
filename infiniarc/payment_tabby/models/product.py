from odoo import fields, models, api, _


class ProductDescriptionTabby(models.Model):
    _inherit = 'product.template'

    tabby = fields.Boolean(string='Available For Tabby')








