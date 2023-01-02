from odoo import models, fields, api, _


class ProductModel(models.Model):
    _name = 'product.model'
    _rec_name = 'name'

    name = fields.Char(string='Name')
