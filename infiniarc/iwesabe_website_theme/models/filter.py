from odoo import fields, models, api, _
from odoo.tools.populate import compute
import json


class DesktopFilter(models.Model):
    _name = 'desktop.filter'
    _description = 'Desktop filter'

    name = fields.Char(string='Name', required=True)
    type = fields.Many2one('product.filter', string='PC Type')
    value_ids = fields.One2many('desktop.filter.line', 'value_id')


class SpecialOfferFilter(models.Model):
    _name = 'special.filter'
    _description = 'Special Offer filter'

    name = fields.Char(string='Name', required=True)
    type = fields.Many2one('special.offer')
    # type = fields.Selection([('gaming', 'Gaming PC'), ('gear', 'Gear Store'), ('stock', 'Stock Clearance')],
    #                         default="gaming", string='PC Type')
    value_ids = fields.One2many('special.filter.line', 'value_id')


class SpecialFilterLine(models.Model):
    _name = 'special.filter.line'
    _rec_name = 'values'
    _description = 'Special filter line'

    value_id = fields.Many2one('special.filter')
    values = fields.Char(string='Values')
    product_id = fields.Many2many('product.template')


class DesktopFilterLine(models.Model):
    _name = 'desktop.filter.line'
    _rec_name = 'values'
    _description = 'Desktop filter line'

    value_id = fields.Many2one('desktop.filter')
    values = fields.Char(string='Values')
    desktop_domain_id = fields.Many2one('product.filter', string="Component", related='value_id.type')
    product_id = fields.Many2many('product.template')
    product_id_domain = fields.Char('Product Domain', compute='_compute_desktop_domain')

    @api.depends('value_id', 'value_id.type')
    def _compute_desktop_domain(self):
        for rec in self:
            component = rec.value_id.type.id
            rec.product_id_domain = json.dumps(
                [('filter_type', '=', rec.desktop_domain_id.id)]
            )


class InfiniarcComponentFilter(models.Model):
    _name = 'component.filter'
    _rec_name = 'filter'
    _description = 'Component Filter'

    filter = fields.Char(string='Name', required=True)
    component_id = fields.Many2one('component.type', string="Component")
    values = fields.Char(string='Values')
    product_ids = fields.One2many('component.filter.line', 'value_id')


class ComponentFilterLine(models.Model):
    _name = 'component.filter.line'
    _description = 'Component Filter Line'

    value_id = fields.Many2one('component.filter')
    values = fields.Char(string='Values')
    component_domain_id = fields.Many2one('component.type', string="Component", related='value_id.component_id')
    product_id = fields.Many2many('product.template')
    product_id_domain = fields.Char('Product Domain', compute='_compute_component_domain')

    @api.depends('value_id', 'value_id.component_id')
    def _compute_component_domain(self):
        for rec in self:
            component = rec.value_id.component_id.id
            rec.product_id_domain = json.dumps(
                [('component_id', '=', rec.component_domain_id.id)]
            )
