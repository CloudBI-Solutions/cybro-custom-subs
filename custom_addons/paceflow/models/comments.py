# -*- coding: utf-8 -*-
"""comments"""

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from random import randint
from dateutil.relativedelta import relativedelta


class Comments(models.Model):
    """model for managing comments"""
    _name = "comment.comment"
    _description = "Comments"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    description = fields.Html(string="Description", required=True)
    legality = fields.Boolean(string="Legality Comment", default=False,
                              store=True,)
    momentum = fields.Boolean(string="Momentum Comment", default=False,
                              store=True,)
    stability = fields.Boolean(string="Stability Comment", default=False,
                               store=True,)
    stability_rear = fields.Boolean(string="Stability rear view Comment",
                                    default=False, store=True,)
    stability_side = fields.Boolean(string="Stability side view Comment",
                                    default=False, store=True,)
    paceflow = fields.Boolean(string="Paceflow Comment", default=False,
                              store=True,)
    paceflow_rear = fields.Boolean(string="Paceflow rear view Comment",
                                   default=False, store=True,)
    paceflow_side = fields.Boolean(string="Paceflow side view Comment",
                                   default=False, store=True,)
    is_category = fields.Boolean('Is a category', default=False)
    order_sequence = fields.Integer()
