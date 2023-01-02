# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
import json


class BrandBrand(models.Model):
    _name = "brand.brand"
    _description = 'Product Brand'

    name = fields.Char('Name')
    code = fields.Char('Code')
    field_name = fields.Char('Field Name')
    micro_store_id = fields.Many2one('dynamic.micro.store', string="Dynamic Micro Store")

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.field_name = self.name.lower()
