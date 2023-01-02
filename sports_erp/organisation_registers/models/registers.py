from odoo import models, fields
import datetime


class Registers(models.Model):
    _name = 'organisation.registers'

    name = fields.Char()
    coach_id = fields.Many2one('organisation.coaches')
    group_id = fields.Many2one('athlete.groups')
    date = fields.Date()
    event_id = fields.Many2one('calendar.event')
    start_date = fields.Datetime(related='event_id.start')
    stop_date = fields.Datetime(related='event_id.stop')
    attendee_ids = fields.One2many('organisation.registers.attendees', 'registers_id')
    # code = fields.Char(index=True)

    def _cron_create_organisation_registers(self):
        """
        This is a cron job that will create a new organisation register.
        """
        start_of_day = datetime.datetime.combine(fields.Date.today(),
                                  datetime.time(00, 00, 00))
        end_of_day = datetime.datetime.combine(fields.Date.today(),
                                  datetime.time(23, 59, 59))
        events = self.env['calendar.event'].sudo().search([('start', '>=', start_of_day), ('start', '<=', end_of_day)])

        for event in events.filtered(lambda x: not x.register_id):
            athletes = self.env['organisation.athletes'].sudo().search(
                [('partner_id', 'in', event.partner_ids.ids)])
            values = {
                'name': event.name,
                'coach_id': event.group_coach_id.id,
                'date': fields.Date.today(),
                'group_id': event.group_id.id,
                'attendee_ids': [
                    (0, 0, {'attendee_id': attendee}) for attendee in
                    athletes.ids
                ],
                'event_id': event.id,
            }
            register_id = self.env['organisation.registers'].sudo().create(
                values)
            event.register_id = register_id.id
            print("events", event)



class RegistersAttendees(models.Model):
    _name = 'organisation.registers.attendees'

    attendee_id = fields.Many2one('organisation.athletes')
    registers_id = fields.Many2one('organisation.registers')
    is_attended = fields.Boolean()


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    register_id = fields.Many2one('organisation.registers')
    group_id = fields.Many2one('athlete.groups')
    group_coach_id = fields.Many2one('organisation.coaches')