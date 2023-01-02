# -*- coding: utf-8 -*-
"""Booking"""


from odoo import fields, models, api, _
from datetime import datetime
from odoo import SUPERUSER_ID
from odoo.exceptions import ValidationError
from datetime import timedelta
import pytz


class Booking(models.Model):
    """model for managing assessments"""
    _name = "booking.booking"
    _description = "Booking"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'sequence'

    sequence = fields.Char(string='Reference', required=True, copy=False,
                           readonly=True, default=lambda self: _('New'),
                           store=True)
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    user_id = fields.Many2one('res.users', string="Responsible",
                              default=lambda self: self.env.user)
    active = fields.Boolean('Active', default=True)
    date = fields.Date('Date', required=True, index=True,
                       default=fields.Date.context_today)
    event_start = fields.Datetime('Start', copy=False, tracking=True,
                                  readonly=True, related='event_id.start')
    event_stop = fields.Datetime('Stop', copy=False, tracking=True,
                                 related='event_id.stop')
    duration = fields.Float(string="Duration", copy=False, tracking=True,
                            readonly=True,
                            related='appointment_type_id.duration')
    event_id = fields.Many2one('calendar.event', string="Event", copy=False,
                               tracking=True)
    venue_id = fields.Many2one('organisation.venues', string="Venue",
                               copy=False,
                               related="appointment_type_id.venue_id")
    coach_id = fields.Many2one('organisation.coaches', string="Coach",
                               copy=False,
                               related="appointment_type_id.coach_id")
    assigned_user_id = fields.Many2one(
        'res.users', string="Assigned to", tracking=True, domain=[
            ('partner_id.org_group_selection', 'in',
             ['ex_coaches', 'parents', 'athletes', 'fans'])],
        default=lambda self: self.env.user)
    assigned_partner_id = fields.Many2one('res.partner',
                                          related='assigned_user_id.partner_id')
    user_ids = fields.Many2many('res.users', string="Attendees", tracking=True,
                                copy=False)
    state = fields.Selection([('enquiry', 'Enquiry'),
                              ('follow_up', 'Follow-up'),
                              ('booked', 'Booked'), ('done', 'Done'),
                              ('cancel', 'Cancel')],
                             string='State', readonly=True, default='enquiry')
    stage_id = fields.Many2one(
        'booking.stage', string='Stage', index=True, tracking=True,
        readonly=False, store=True, copy=False, ondelete='restrict',
        default=lambda self: self._default_stage_id(),
        group_expand='_read_group_stage_ids')
    appointment_type_id = fields.Many2one('booking.type',
                                          string='Appointment type')
    date_done = fields.Date('Done date', readonly=True, copy=False)
    date_cancel = fields.Date('Cancel date', readonly=True, copy=False)
    is_mailed = fields.Boolean(string="Is mailed", default=False, readonly=True)
    description = fields.Text(string="Description", copy=False)
    lead_id = fields.Many2one('crm.lead', string="Lead")

    def notify_user(self, res):
        coach = res.coach_id
        title = _("Booking Created")
        message = _("Ref %s", res.sequence)
        self.env['bus.bus'].sendone(
            (self._cr.dbname, 'res.partner', coach.partner_id.id),
            {'type': 'user_connection', 'title': title,
             'message': message, 'partner_id': res.user_id.partner_id.id}
        )

    @api.model
    def create(self, vals):
        if not vals.get('sequence') or vals['sequence'] == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'booking.booking') or _('New')
        res = super(Booking, self).create(vals)
        notification_ids = []
        partner_ids = []
        name = res.sequence
        author_id = res.assigned_user_id.partner_id.id
        if res.appointment_type_id:
            coach = res.appointment_type_id.coach_id
            partner_ids.append(coach.partner_id.id)
            notification_ids.append((0, 0, {
                'res_partner_id': coach.partner_id.id,
                'notification_type': 'inbox'
            }))
            res.message_post(body='Appointment scheduled...',
                             subject=name,
                             message_type='notification',
                             subtype_xmlid='mail.mt_comment',
                             partner_ids=partner_ids,
                             author_id=author_id,
                             notification_ids=notification_ids)
            self.notify_user(res)
            return res

    def action_create_lead(self):
        lead = self.env['crm.lead'].create({
            'name': self.sequence,
            'partner_id': self.assigned_partner_id.id,
            'type': 'opportunity',
        })
        self.lead_id = lead

    def action_book(self):
        book_stage = self.env['booking.stage'].search(
            [('name', 'ilike', 'Booked')])
        self.write({'state': 'booked',
                    'stage_id': book_stage.id})

    def action_cancel(self):
        if self.event_id:
            self.env['calendar.event'].search(
                [('id', '=', self.event_id.id)]).sudo().unlink()
        cancel_stage = self.env['booking.stage'].search(
            [('name', 'ilike', 'Cancel')])
        self.write({'state': 'cancel',
                    'stage_id': cancel_stage.id,
                    'date_cancel': fields.Date.today()})

    def action_follow_up(self):
        follow_up_stage = self.env['booking.stage'].search(
            [('name', 'ilike', 'Follow-up')])
        self.write({'state': 'follow_up',
                    'stage_id': follow_up_stage.id})

    def action_send_mail(self):
        if not self.assigned_user_id:
            raise ValidationError("Please assign this booking before "
                                  "sending mail!!")
        template_id = self.env.ref('booking.booking_assign_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.write({
            'is_mailed': True,
        })

    def action_open_calendar(self):
        return {
            'name': "Calendar",
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'view_mode': 'calendar',
            'context': {'create': True, 'booking_id': self.id}
        }

    def action_open_event(self):
        return {
            'name': "Calendar",
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'view_mode': 'form',
            'res_id': self.event_id.id,
            'context': {'create': False}
        }

    @api.model
    def _compute_done(self):
        bookings = self.env['booking.booking'].search([])
        for booking in bookings:
            if booking.event_id and booking.event_stop < fields.Datetime.now():
                done_stage = self.env['booking.stage'].search(
                    [('name', 'ilike', 'Done')])
                booking.write({
                    'state': 'done',
                    'stage_id': done_stage.id,
                    'date_done': fields.Date.today()
                })

    @api.model
    def _compute_archive(self):
        bookings = self.env['booking.booking'].search([])
        for booking in bookings:
            today = fields.Date.today()
            if booking.state == 'done':
                from_date = datetime.strptime(str(booking.date_done), "%Y-%m-%d")
                to_date = datetime.strptime(str(today), "%Y-%m-%d")
                difference = (to_date - from_date).days
                if difference > 30:
                    booking.write({
                        'active': False,
                    })
            elif booking.state == 'cancel':
                from_date = datetime.strptime(str(booking.date_cancel),
                                              "%Y-%m-%d")
                to_date = datetime.strptime(str(today), "%Y-%m-%d")
                difference = (to_date - from_date).days
                if difference > 30:
                    booking.write({
                        'active': False,
                    })
            else:
                return

    def _default_stage_id(self):
        """Setting default stage"""
        rec = self.env['booking.stage'].search(
            [], limit=1, order='sequence ASC')
        return rec.id if rec else None

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Read all the stages and display it in the kanban view,
            even if it is empty."""
        stage_ids = stages._search([], order=order,
                                          access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)


class BookingStages(models.Model):
    """ Stages of Booking """
    _name = "booking.stage"
    _description = "Booking Stages"
    _order = "sequence, id"
    _rec_name = "name"

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1,
                              help="Used to order stages. Lower is better.")
    description = fields.Text(string='Description', translate=True)
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when '
                               'there are no records in that stage to display.')

    _sql_constraints = [('number_name', 'UNIQUE (name)',
                         'You can not have two stages with the same Name !')]


class BookingType(models.Model):
    """ Types of Booking """
    _name = "booking.type"
    _description = "Booking Type"
    _rec_name = "name"

    name = fields.Char('Stage Name', required=True, translate=True, copy=False)
    description = fields.Text(string='Description', translate=True, copy=False)
    duration = fields.Float(string="Duration", required=True, copy=False)
    venue_id = fields.Many2one('organisation.venues', string="Venue",
                               required=True, copy=False)
    coach_id = fields.Many2one('organisation.coaches', string="Coach",
                               required=True, copy=False)

    _sql_constraints = [('number_name', 'UNIQUE (name)',
                         'You can not have two stages with the same Name !')]

