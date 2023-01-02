# -*- coding: utf-8 -*-
"""child"""

from odoo import fields, models, api
from datetime import datetime


class Child(models.Model):
    """model for managing child"""
    _name = "paceflow.child"
    _description = "Player"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="First Name",
                       related='partner_id.name',
                       readonly=True)
    last_name = fields.Char(string="Last Name",
                            related='partner_id.last_name',
                            readonly=True)
    image_1920 = fields.Image(related='partner_id.image_1920')
    dob = fields.Date(string="DOB", required=True)
    partner_id = fields.Many2one('res.partner', string="Name")
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email", required=True)
    user_id = fields.Many2one('res.users', string="User")
    highest_standard = fields.Selection(
        [('professional', 'Professional'),
         ('country_academy', 'Country Academy'),
         ('country_age_group', 'Country Age Group'),
         ('club_cricket', 'Club Cricket'),
         ('non_competitive', 'Non-Competitive')],
        string="Highest Standard Played")

    coach_ids = fields.Many2many('paceflow.client', 'child_coach_rel',
                                 'child_id', 'coach_id', string='Coach')
    group_ids = fields.Many2many('paceflow.child.group', 'child_group_rel',
                                 'child_id', 'group_id', string='Group')
    parent_ids = fields.Many2many('paceflow.parents', 'child_parent_rel',
                                  'child_id', 'parent_id', string='Parents')
    invoice_ids = fields.Many2many('account.move', 'child_invoice_rel',
                                   'child_id', 'invoice_id', string="Invoices",
                                   compute="_compute_invoices")

    def _compute_invoices(self):
        self.invoice_ids = self.partner_id.invoice_ids

    @api.model
    def create(self, vals):
        """create method"""
        result = super(Child, self).create(vals)
        result.partner_id.write({'is_child': True})
        return result

    def view_client(self):
        """methode for smart button"""
        parent = self.env['paceflow.client'].search([
            ('child_ids', 'in', self.ids)])
        print('parent', parent)
        return {
            'name': "Client",
            'type': 'ir.actions.act_window',
            'res_model': 'paceflow.client',
            'res_id': parent.id,
            'view_mode': 'form',
            'domain': [('id', '=', parent.id)]
        }

    @api.model
    def get_dob(self, child_id):
        child = self.env['paceflow.child'].browse(int(child_id))
        if child:
            dob = datetime.strftime(child.dob, '%d/%m/%Y')
            return {'dob': dob}
