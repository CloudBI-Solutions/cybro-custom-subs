# -*- coding: utf-8 -*-
"""clients"""

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from random import randint
from dateutil.relativedelta import relativedelta


class Clients(models.Model):
    """model for managing clients"""
    _name = "paceflow.client"
    _description = "Coach"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'partner_id'

    name = fields.Char(string="Name", related='partner_id.name', readonly=True)
    last_name = fields.Char(string="Last name", related='partner_id.last_name')
    image_1920 = fields.Image(related='partner_id.image_1920')
    partner_id = fields.Many2one('res.partner', string="Name", required=True)
    phone = fields.Char(string="Phone",
                        related='partner_id.phone', required=True)
    email = fields.Char(string="Email",
                        related='partner_id.email', required=True)
    user_id = fields.Many2one('res.users', string="User")
    child_ids = fields.Many2many('paceflow.child', 'client_child_rel',
                                 'client_id', 'child_id',
                                 string="Player contacts")
    group_ids = fields.Many2many('paceflow.child.group', 'client_group_rel',
                                 'client_id', 'group_id', string="Groups")
    invoice_ids = fields.Many2many('account.move', 'client_invoice_rel',
                                   'client_id', 'invoice_id', string="Invoices",
                                   compute="_compute_invoices")

    def _compute_invoices(self):
        child_partners = []
        for child in self.child_ids:
            child_partners.append(child.partner_id.id)

    @api.model
    def create(self, vals):
        """methode to handle pace-flow courses"""
        result = super(Clients, self).create(vals)
        result.partner_id.write({'is_client': True})
        courses = self.env['slide.channel'].search(
            [('is_paceflow_course', '=', True),
             ('partner_ids', 'not in', result.partner_id.id)])
        for course in courses:
            self.env['slide.channel.partner'].create({
                'channel_id': course.id,
                'partner_id': result.partner_id.id, })
        return result


class SaleOrder(models.Model):
    """inherited sale order"""
    _inherit = 'sale.order'

    def _default_user_ids(self, partner_id):
        """methode to grant portal access"""
        welcome_message = ""
        contact_ids = set()
        user_changes = []
        partner = self.env['res.partner'].sudo().browse(partner_id)
        contact_partners = partner.child_ids.filtered(lambda p: p.type in ('contact', 'other')) | partner
        wizard_id = self.env['portal.wizard'].create(
            {'welcome_message': welcome_message})
        for contact in contact_partners:
            # make sure that each contact appears at most once in the list
            if contact.id not in contact_ids:
                contact_ids.add(contact.id)
                user_changes.append(({
                    'wizard_id': wizard_id.id,
                    'partner_id': contact.id,
                    'email': contact.email,
                    'in_portal': True,
                }))
        return user_changes

    def action_confirm(self):
        """override prepare_invoice function to include branch"""
        res = super(SaleOrder, self).action_confirm()
        partner = self.partner_id
        paceflow_product = self.env['product.product'].sudo().browse(
                           self.env.ref('paceflow.paceflow_package').id)
        for line in self.order_line:
            if line.product_id == paceflow_product:
                client = self.env['paceflow.client'].sudo().search(
                    [('partner_id', '=', partner.id)])
                if not client:
                    self.env['paceflow.client'].sudo().create(
                        {
                            'partner_id': partner.id,
                        })
                    partner.sudo().write({
                        'is_client': True,
                    })
                    user_ids = self.env['portal.wizard.user'].create(
                        self._default_user_ids(self.partner_id.id))
                    user_ids.action_apply()
        return res
