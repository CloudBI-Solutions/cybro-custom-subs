
from odoo import api, models, fields, _
import json
from odoo.exceptions import UserError, ValidationError


class OrderlineMo(models.Model):
    _inherit = "sale.order.line"
    _description = "Sales Order Line"

    created_mo_id = fields.Many2one('mrp.production',
                                            'Created Manufacturing Order')

    created_bom_id = fields.Many2one('mrp.bom',
                                            'Created BOM')
    website_customized = fields.Boolean()