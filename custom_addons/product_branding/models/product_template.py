from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_name = fields.Char()
