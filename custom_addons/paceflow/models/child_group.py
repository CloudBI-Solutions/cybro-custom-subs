# -*- coding: utf-8 -*-
"""child_group"""

from odoo import fields, models, api


class ChildGroup(models.Model):
    """model for managing group"""
    _name = "paceflow.child.group"
    _description = "Group"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
