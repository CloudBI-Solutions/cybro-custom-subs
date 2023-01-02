# -*- coding: utf-8 -*-

from ast import literal_eval
from odoo import models, fields, api, _
from odoo.addons.auth_signup.models.res_partner import SignupError
from odoo.tools.misc import ustr


class CalendarChecklist(models.Model):
    _name = "calendar.checklist"
    _description = "Calendar Checklist"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description")
    state = fields.Selection([('new', 'New'), ('completed', 'Completed')],
                             string="State",
                             default='new',
                             readonly=True,
                             index=True)
    partner_id = fields.Many2one('res.partner', copy=False)
    event_id = fields.Many2one('calendar.event', copy=False)

    def btn_check(self):
        for rec in self:
            rec.write({'state': 'completed'})


class Events(models.Model):
    _inherit = "calendar.event"

    has_booking = fields.Boolean(string="Booking Checklist", default=False)
    venue_id = fields.Many2one('organisation.venues', string="Venue",
                               copy=False)
    coach_id = fields.Many2one('organisation.coaches', string="Coach",
                               copy=False)
    event_description = fields.Char("description",
                                    compute="compute_event_description")
    booking_id = fields.Many2one('booking.booking', string="Booking")
    checklist_ids = fields.Many2many("calendar.checklist",
                                     'checklist_calendar_rel',
                                     'event_id', 'checklist_id',
                                     string="Checklist")
    checklist = fields.Float("Checklist Completed",
                             compute="_compute_checklist")
    is_web_create = fields.Boolean(string="Is created through website",
                                   default=False, readonly=True)

    @api.model
    def create(self, vals_list):
        result = super(Events, self).create(vals_list)
        if result.has_booking:
            if self.env.context.get('booking_id'):
                result.booking_id = self.env.context.get('booking_id')
                booking = self.env['booking.booking'].search(
                    [('id', '=', self.env.context.get('booking_id'))])
                booking.write({
                    'event_id': result.id
                })
        o_checklists = self.env['calendar.checklist'].search(
            [('event_id', '=', self.id)])
        o_checklists.sudo().unlink()
        partners = result.partner_ids
        if partners:
            for partner in partners:
                new_checklist_vals = {
                    'name': partner.name,
                    'state': 'new',
                    'partner_id': partner.id,
                    'event_id': result.id
                }
                self.env['calendar.checklist'].create(new_checklist_vals)
            checklists = self.env['calendar.checklist'].search(
                [('event_id', '=', result.id)])
            result.checklist_ids = checklists
        return result

    def write(self, vals):
        if 'partner_ids' in vals:
            partner_ids = vals['partner_ids'][0][2]
            checklist_ids = []
            for partner_id in partner_ids:
                partner = self.env['res.partner'].search([
                    ('id', '=', partner_id)
                ])
                checklist = self.env['calendar.checklist'].search(
                    [('event_id', '=', self.id),
                     ('partner_id', '=', partner_id)])
                if checklist:
                    checklist_ids.append(checklist.id)
                else:
                    new_checklist_vals = {
                        'name': partner.name,
                        'state': 'new',
                        'partner_id': partner.id,
                        'event_id': self.id
                    }
                    checklist = self.env['calendar.checklist'].create(
                        new_checklist_vals)
                    checklist_ids.append(checklist.id)
            checklists = self.env['calendar.checklist'].search(
                    [('event_id', '=', self.id)])
            for checklist in checklists:
                if checklist.id not in checklist_ids:
                    unlink_checklist = checklist = self.env[
                        'calendar.checklist'].search(
                        [('id', '=', checklist.id)])
                    unlink_checklist.sudo().unlink()
            vals.update({
                'checklist_ids': [[6, False, checklist_ids]]
            })
        result = super(Events, self).write(vals)
        return result

    @api.depends('checklist_ids')
    def _compute_checklist(self):
        for rec in self:
            checklists = self.env['calendar.checklist'].search(
                [('event_id', '=', rec.id)])
            total_cnt = len(checklists)
            if total_cnt:
                checked = self.env['calendar.checklist'].search(
                    [('event_id', '=', rec.id), ('state', '=', 'completed')])
                checked_cnt = len(checked)
                if checked_cnt == 0:
                    rec.checklist = 0
                else:
                    checklist_perc = (checked_cnt/total_cnt)
                    rec.checklist = checklist_perc
            else:
                rec.checklist = 0

    @api.depends('name', 'coach_id', 'venue_id', 'description')
    def compute_event_description(self):
        for rec in self:
            description = 'Title :  %s\n' % rec.name
            if rec.venue_id:
                description += 'Venue :  %s\n' % rec.venue_id.name
            if rec.coach_id:
                description += 'Coach :  %s\n' % rec.coach_id.name
            if rec.description:
                description += 'Description :  %s\n' % rec.description
            rec.event_description = description


class Partner(models.Model):
    _inherit = "res.partner"

    booking_ids = fields.One2many('booking.booking', 'assigned_partner_id',
                                  string="Bookings")


class Users(models.Model):
    _inherit = "res.users"

    @api.model_create_multi
    def create(self, vals_list):
        users = super(Users, self).create(vals_list)
        if 'website_id' in self.env.context:
            group_portal = self.env.ref('base.group_portal')
            for user in users:
                user.write({
                    'groups_id': [(6, 0, [group_portal.id])]
                })
                partner = user.partner_id
                if not partner.org_group_selection:
                    self.env['organisation.fans'].sudo().create({
                        'partner_id': partner.id
                    })
                    partner.write({
                        'create_booking': True
                    })
        return users

    def _create_user_from_template(self, values):
        template_user_id = literal_eval(self.env['ir.config_parameter'].sudo().get_param('base.template_portal_user_id', 'False'))
        template_user = self.browse(template_user_id)
        if not template_user.exists():
            raise ValueError(_('Signup: invalid template user'))

        if not values.get('login'):
            raise ValueError(_('Signup: no login given for new user'))
        if not values.get('partner_id') and not values.get('name'):
            raise ValueError(_('Signup: no name or partner given for new user'))

        # create a copy of the template user (attached to a specific partner_id if given)
        values['active'] = True
        try:
            with self.env.cr.savepoint():
                user = template_user.with_context(no_reset_password=True).copy(values)
                partner = user.partner_id
                if not partner.org_group_selection:
                    self.env['organisation.fans'].sudo().create({
                        'partner_id': partner.id
                    })
                    partner.write({
                        'create_booking': True
                    })
                # return template_user.with_context(no_reset_password=True).copy(values)
                return user
        except Exception as e:
            # copy may failed if asked login is not available.
            raise SignupError(ustr(e))


class Lead(models.Model):
    _inherit = "crm.lead"

    product_ids = fields.Many2many('product.template', 'lead_product_rel',
                                   'lead_id', 'product_id', string="Products")
    expected_revenue = fields.Monetary(compute='_compute_expected_revenue',
                                       readonly=False, store=True)

    @api.depends('product_ids')
    def _compute_expected_revenue(self):
        for lead in self:
            if not lead.product_ids:
                lead.expected_revenue = 0
            else:
                products = lead.product_ids
                revenue = 0
                for product in products:
                    revenue += product.list_price
                lead.expected_revenue = revenue


