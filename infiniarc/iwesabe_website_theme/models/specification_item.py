# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
import json
from odoo.exceptions import UserError, ValidationError


class SpecificationItem(models.Model):
    _name = "specification.item"
    _description = "Specification Item"

    sequence = fields.Integer(index=True,
                              help="Gives the sequence order when displaying a list of bank statement lines.",
                              default=1)
    name = fields.Char('Name')


class SpecificationItemLine(models.Model):
    _name = "specification.item.line"
    _description = "Specification Item Line"

    sequence = fields.Integer('Sequence', default=1, tracking=True)
    name = fields.Char('Value')
    item_id = fields.Many2one("component.type", string="Item")
    product_id = fields.Many2one("product.template", string="Product")


class CPUTYPE(models.Model):
    _name = "cpu.type"
    _description = "CPU Type"

    name = fields.Char('Name')


class MemoriesType(models.Model):
    _name = "memories.type"
    _description = "Memories Type"

    name = fields.Char('Name')


class RadiatorSizeValues(models.Model):
    _name = "radiator.size.values"
    _description = "Radiator Size Values"

    name = fields.Integer('Name')
