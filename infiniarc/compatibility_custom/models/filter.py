from odoo import fields, models, api, _


class ProductFilterView(models.Model):
    _name = 'product.filter'
    _rec_name = 'filter'

    filter = fields.Char(string='filter')
    active = fields.Boolean(string='Active', default=True)
    website_id = fields.Many2one('website')


class WebsiteFilterProduct(models.Model):
    _inherit = 'website'

    filter_ids = fields.One2many('product.filter', 'website_id', string='Filter')
