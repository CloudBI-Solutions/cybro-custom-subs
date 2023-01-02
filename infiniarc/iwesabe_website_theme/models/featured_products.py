from odoo import fields, models, api, _


class FeaturedProducts(models.Model):
    _name = 'featured.product'
    _description = 'Featured Products'

    name = fields.Char(string='Name')

    featured_product_ids = fields.One2many('featured.product.line', 'feature_id', string='Featured Products')
    single_ids = fields.One2many('single.product.line', 'single_id', string='Single Products')


class FeaturedProductsLine(models.Model):
    _name = 'featured.product.line'
    _description = 'Featured Product Line'

    featured_product = fields.Many2one('product.template', string='product')
    feature_id = fields.Many2one('featured.product')


class SingleProductLine(models.Model):
    _name = 'single.product.line'
    _description = 'Single Product Line'

    single_product = fields.Many2one('product.template', string='product')
    single_id = fields.Many2one('featured.product')


# class FeaturedProductTemplate(models.Model):
#     _inherit = 'product.template'

