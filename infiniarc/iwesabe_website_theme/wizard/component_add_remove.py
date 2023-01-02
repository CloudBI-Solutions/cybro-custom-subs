# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError, ValidationError


class ComponentAddRemove(models.TransientModel):
    _name = "component.add.remove"

    @api.model
    def default_get(self, fields):
        res = super(ComponentAddRemove, self).default_get(fields)
        active_id = self._context.get('active_id', False)
        default_type = self._context.get('default_type', False)

        if active_id:
            active_id = self.env['component.line'].browse(active_id)
            if default_type == 'add':
                product_line = active_id.component_id.product_line.ids
                selected_line = active_id.product_ids.ids
                unselected_product = set(product_line) - set(selected_line)
                component_lines = []
                if unselected_product:
                    unselected_products = self.env['product.product'].browse(unselected_product)
                    for product in unselected_products:
                        component_lines.append((0, 0, {'product_id': product.id}))
                res['component_lines'] = component_lines
            else:
                selected_line = active_id.product_ids
                component_lines = []
                for product in selected_line:
                    component_lines.append((0, 0, {'product_id': product.id}))
                res['component_lines'] = component_lines
        return res

    component_lines = fields.One2many('component.add.remove.line', 'component_id', string='Components')
    type = fields.Selection([('add', 'ADD'), ('remove', 'Remove')], 'Type')
    allowed = fields.Boolean('Select All')

    def action_submit(self):
        active_id = self._context.get('active_id', False)
        if not self.component_lines:
            raise UserError(_("Not Found Any Records!!!"))
        if active_id:
            active_id = self.env['component.line'].browse(active_id)
            if self.type == 'add':
                product_list = []
                for p in self.component_lines:
                    if p.allowed:
                        active_id.product_ids = [(4, p.product_id.id)]
            else:
                product_list = []
                for p in self.component_lines:
                    if p.allowed:
                        active_id.product_ids = [(3, p.product_id.id)]
            active_id.get_default_product()

    @api.onchange('allowed')
    def action_select(self):
        for rec in self.component_lines:
            if self.allowed:
                rec.allowed = True
            else:
                rec.allowed = False


class ComponentAddRemoveLine(models.TransientModel):
    _name = "component.add.remove.line"

    allowed = fields.Boolean('CheckBox')
    component_id = fields.Many2one('component.add.remove', 'Component')
    product_id = fields.Many2one('product.product', string="Products")
    barcode = fields.Char(related="product_id.barcode", string='Barcode', store=True)
    list_price = fields.Float(related="product_id.list_price", string='Sale Price', store=True)
    standard_price = fields.Float(related="product_id.standard_price", string='Cost Price', store=True)
    qty_available = fields.Float(related="product_id.qty_available", string='Quantity On Hand', store=True)
