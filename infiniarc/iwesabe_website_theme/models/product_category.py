# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
import json


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    def get_product_by_categ(self):
        product_id = self.env['product.template'].search([('public_categ_ids', '=', self.id)], limit=1)
        return product_id if product_id else False

    def get_productmulti_by_categ(self):
        product_id = self.env['product.template'].search([('public_categ_ids', '=', self.id)], limit=3)
        return product_id if product_id else False
