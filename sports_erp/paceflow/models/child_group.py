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
    image_1920 = fields.Image(string='Group Image')

    child_ids = fields.Many2many('paceflow.child', 'group_child_rel',
                                 'group_id', 'child_id', string='Players')

    def select_coach(self):
        user_id = self.env.user
        partner_id = user_id.partner_id
        coach = self.env['paceflow.client'].search([
            ('partner_id', '=', partner_id.id)
        ])
        return coach.id

    responsible_user = fields.Many2one('paceflow.client',
                                       default=select_coach,
                                       string="Responsible Coach")

