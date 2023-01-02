# -*- coding: utf-8 -*-
"""parents"""

from odoo import fields, models, api, _


class Parents(models.Model):
    _name = "paceflow.parents"
    _description = "Parents"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Name",
                       related='partner_id.name',
                       readonly=True)
    last_name = fields.Char(string="Last Name",
                            related='partner_id.last_name',
                            readonly=True)
    coach_id = fields.Many2one('paceflow.client', string="Coach Id",
                               readonly=True)
    partner_id = fields.Many2one('res.partner', string='Name')
    image_1920 = fields.Image(related='partner_id.image_1920')
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone", required=True)
    emergency_number = fields.Char(string="Emergency Number", required=True)
    child_ids = fields.Many2many('paceflow.child', 'parent_child_rel',
                                 'parent_id', 'child_id', string='Child')
    invoice_ids = fields.Many2many('account.move', 'parent_invoice_rel',
                                   'parent_id', 'invoice_id', string="Invoices",
                                   compute="_compute_invoices")

    def _compute_invoices(self):
        child_partners = []
        for child in self.child_ids:
            child_partners.append(child.partner_id.id)
        invoices = self.env['account.move'].search([
                                ('partner_id', 'in', child_partners)])
        self.invoice_ids = invoices.ids + self.partner_id.invoice_ids.ids
