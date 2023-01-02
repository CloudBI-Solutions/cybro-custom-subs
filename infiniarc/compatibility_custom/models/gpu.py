from odoo import fields, models, api, _


class ProductFilterView(models.Model):
    _name = 'gpu.gpu'
    _rec_name = 'name'

    name = fields.Char(string='Name')
