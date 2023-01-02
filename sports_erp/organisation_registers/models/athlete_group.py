from odoo import models,fields
import datetime
from datetime import datetime
import pytz
from datetime import timedelta


class AthleteGroups(models.Model):
    _inherit = 'athlete.groups'

    coach_ids = fields.Many2many('organisation.coaches')
    venue_id = fields.Many2one('organisation.venues')
    mon_schedule_ids = fields.One2many('group.mon.schedule', 'group_id')
    tue_schedule_ids = fields.One2many('group.tue.schedule', 'group_id')
    wed_schedule_ids = fields.One2many('group.wed.schedule', 'group_id')
    thu_schedule_ids = fields.One2many('group.thu.schedule', 'group_id')
    fri_schedule_ids = fields.One2many('group.fri.schedule', 'group_id')
    sat_schedule_ids = fields.One2many('group.sat.schedule', 'group_id')
    sun_schedule_ids = fields.One2many('group.sun.schedule', 'group_id')
    mon = fields.Boolean('Monday')
    tue = fields.Boolean('Tuesday')
    wed = fields.Boolean('Wednesday')
    thu = fields.Boolean('Thursday')
    fri = fields.Boolean('Friday')
    sat = fields.Boolean('Saturday')
    sun = fields.Boolean('Sunday')

    def get_time_from_slot(self, time):
        result = '{0:02.0f}:{1:02.0f}'.format(*divmod(time * 60, 60))
        return result


class MonSchedule(models.Model):
    _name = 'group.mon.schedule'

    name = fields.Char(string="Training Name")
    mon_from = fields.Float(string="From")
    mon_to = fields.Float(string="To")
    venue_id = fields.Many2one('organisation.venues')
    is_recurrent = fields.Boolean(string="Recurrent")
    is_cancel = fields.Boolean(string="Is Cancelled?")
    group_id = fields.Many2one('athlete.groups')
    calendar_event_ids = fields.Many2many('calendar.event')

    def create(self, vals):
        res = super(MonSchedule, self).create(vals)
        for rec in res:
            partner_ids = []
            # group_coach = self.env['organisation.coaches'].sudo().search([('partner_id', '=', rec.group_id.responsible_user_id.partner_id.id)])
            # print(group_coach, "coach")
            athlete_partners = rec.group_id.athlete_ids.mapped('partner_id').ids
            coach_partners = rec.group_id.coach_ids.mapped('partner_id').ids
            group_coach = rec.group_id.coach_ids.mapped('id')[0]
            print(group_coach)
            for athlete_partner in athlete_partners:
                partner_ids.append(athlete_partner)
            for coach in coach_partners:
                partner_ids.append(coach)
            weekday = 0  ## Monday
            dt = datetime.now().replace(hour=0, minute=0,
                                                 second=0,microsecond=0)  ## or any specific date
            days_remaining = (weekday - dt.weekday() - 1) % 7 + 1
            next_dt = dt + timedelta(days_remaining)
            time_from = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.mon_from * 60, 60))
            time_to = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.mon_to * 60, 60))
            next_dt_str = next_dt.strftime('%Y-%m-%d')
            str_datetime_start = next_dt_str + ' ' + time_from
            str_datetime_end = next_dt_str + ' ' + time_to
            datetime_object = datetime.strptime(str_datetime_start, "%Y-%m-%d %H:%M")
            datetime_object_to = datetime.strptime(str_datetime_end, "%Y-%m-%d %H:%M")
            utc_offset = datetime.now(
                pytz.timezone(self.env.user.tz)).utcoffset().total_seconds()
            hour_utc_offset = utc_offset / 3600
            start = datetime_object + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            stop = datetime_object_to + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            event = self.env['calendar.event'].sudo().create({
                'name': '%s/%s' % (rec.group_id.name,
                                         rec.name,
                                        ),
                'start': start,
                'stop': stop,
                'recurrency': rec.is_recurrent,
                'interval': 1,
                'rrule_type': 'weekly',
                'mon': True,
                'end_type': 'forever',
                # 'duration': duration,
                # 'has_booking': True,
                'venue_id': rec.venue_id.id if rec.venue_id.id else rec.group_id.venue_id.id,
                'group_id': rec.group_id.id,
                'group_coach_id': group_coach,
                # 'user_id': booking_coach_user.id,
                'is_web_create': True,
                'partner_ids': [[6, False, partner_ids]],
            })
            rec.calendar_event_ids = [(4, event.id)]
            print(rec.calendar_event_ids, "calendar event")
        return res

    def unlink(self):
        recurrence = self.env['calendar.recurrence'].sudo().search([('base_event_id', 'in', self.calendar_event_ids.mapped('id'))])
        print("Aaaaa", self.calendar_event_ids, self)
        self.calendar_event_ids.unlink()
        if recurrence:
            print(recurrence, "recurrence")
            recurrence.mapped('calendar_event_ids').unlink()
        return super(MonSchedule, self).unlink()


class TueSchedule(models.Model):
    _name = 'group.tue.schedule'

    name = fields.Char(string="Training Name")
    tue_from = fields.Float(string="From")
    tue_to = fields.Float(string="To")
    venue_id = fields.Many2one('organisation.venues')
    is_recurrent = fields.Boolean(string="Recurrent")
    is_cancel = fields.Boolean(string="Is Cancelled?")
    group_id = fields.Many2one('athlete.groups')
    calendar_event_ids = fields.Many2many('calendar.event')

    def create(self, vals):
        res = super(TueSchedule, self).create(vals)
        print(res, "res")
        for rec in res:
            partner_ids = []
            athlete_partners = rec.group_id.athlete_ids.mapped('partner_id').ids
            coach_partners = rec.group_id.coach_ids.mapped('partner_id').ids
            group_coach = rec.group_id.coach_ids.mapped('id')[0]
            for athlete_partner in athlete_partners:
                partner_ids.append(athlete_partner)
            for coach in coach_partners:
                partner_ids.append(coach)
            weekday = 1  ## Tuesday
            dt = datetime.now().replace(hour=0, minute=0,
                                                 second=0,microsecond=0)  ## or any specific date
            days_remaining = (weekday - dt.weekday() - 1) % 7 + 1
            next_dt = dt + timedelta(days_remaining)
            time_from = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.tue_from * 60, 60))
            time_to = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.tue_to * 60, 60))
            next_dt_str = next_dt.strftime('%Y-%m-%d')
            print(next_dt_str, "next day")
            str_datetime_start = next_dt_str + ' ' + time_from
            str_datetime_end = next_dt_str + ' ' + time_to
            datetime_object = datetime.strptime(str_datetime_start, "%Y-%m-%d %H:%M")
            datetime_object_to = datetime.strptime(str_datetime_end, "%Y-%m-%d %H:%M")
            str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
            utc_offset = datetime.now(
                pytz.timezone(self.env.user.tz)).utcoffset().total_seconds()
            hour_utc_offset = utc_offset / 3600
            start = datetime_object + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            stop = datetime_object_to + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            event = self.env['calendar.event'].sudo().create({
                'name': '%s/%s' % (rec.group_id.name,
                                         rec.name,
                                        ),
                'start': start,
                'stop': stop,
                'recurrency': rec.is_recurrent,
                'interval': 1,
                'rrule_type': 'weekly',
                'tue': True,
                'end_type': 'forever',
                'group_id': rec.group_id.id,
                'group_coach_id': group_coach,
                # 'duration': duration,
                # 'has_booking': True,
                'venue_id': rec.venue_id.id if rec.venue_id.id else rec.group_id.venue_id.id,
                # 'coach_id': appointment_type.coach_id.id,
                # 'user_id': booking_coach_user.id,
                'is_web_create': True,
                'partner_ids': [[6, False, partner_ids]],
            })
            print(event, "event")
            rec.calendar_event_ids = [(4, event.id)]
        return res

    def unlink(self):
        recurrence = self.env['calendar.recurrence'].sudo().search([('base_event_id', 'in', self.calendar_event_ids.mapped('id'))])
        print("Aaaaa", self.calendar_event_ids, self)
        self.calendar_event_ids.unlink()
        if recurrence:
            print(recurrence, "recurrence")
            recurrence.mapped('calendar_event_ids').unlink()
        return super(TueSchedule, self).unlink()


class WedSchedule(models.Model):
    _name = 'group.wed.schedule'

    name = fields.Char(string="Training Name")
    wed_from = fields.Float(string="From")
    wed_to = fields.Float(string="To")
    venue_id = fields.Many2one('organisation.venues')
    is_recurrent = fields.Boolean(string="Recurrent")
    is_cancel = fields.Boolean(string="Is Cancelled?")
    group_id = fields.Many2one('athlete.groups')
    calendar_event_ids = fields.Many2many('calendar.event')

    def create(self, vals):
        res = super(WedSchedule, self).create(vals)
        for rec in res:
            partner_ids = []
            athlete_partners = rec.group_id.athlete_ids.mapped('partner_id').ids
            coach_partners = rec.group_id.coach_ids.mapped('partner_id').ids
            group_coach = rec.group_id.coach_ids.mapped('id')[0]
            for athlete_partner in athlete_partners:
                partner_ids.append(athlete_partner)
            for coach in coach_partners:
                partner_ids.append(coach)
            weekday = 2  ## Wednesday
            dt = datetime.now().replace(hour=0, minute=0,
                                                 second=0,microsecond=0)  ## or any specific date
            days_remaining = (weekday - dt.weekday() - 1) % 7 + 1
            next_dt = dt + timedelta(days_remaining)
            time_from = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.wed_from * 60, 60))
            time_to = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.wed_to * 60, 60))
            next_dt_str = next_dt.strftime('%Y-%m-%d')
            str_datetime_start = next_dt_str + ' ' + time_from
            str_datetime_end = next_dt_str + ' ' + time_to
            datetime_object = datetime.strptime(str_datetime_start, "%Y-%m-%d %H:%M")
            datetime_object_to = datetime.strptime(str_datetime_end, "%Y-%m-%d %H:%M")
            str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
            utc_offset = datetime.now(
                pytz.timezone(self.env.user.tz)).utcoffset().total_seconds()
            hour_utc_offset = utc_offset / 3600
            start = datetime_object + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            stop = datetime_object_to + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            event = self.env['calendar.event'].sudo().create({
                'name': '%s/%s' % (rec.group_id.name,
                                         rec.name,
                                        ),
                'start': start,
                'stop': stop,
                'recurrency': rec.is_recurrent,
                'interval': 1,
                'rrule_type': 'weekly',
                'wed': True,
                'end_type': 'forever',
                'group_id': rec.group_id.id,
                'group_coach_id': group_coach,
                # 'duration': duration,
                # 'has_booking': True,
                'venue_id': rec.venue_id.id if rec.venue_id.id else rec.group_id.venue_id.id,
                # 'coach_id': appointment_type.coach_id.id,
                # 'user_id': booking_coach_user.id,
                'is_web_create': True,
                'partner_ids': [[6, False, partner_ids]],
            })
            print(event, "event")
            rec.calendar_event_ids = [(4, event.id)]
        return res

    def unlink(self):
        recurrence = self.env['calendar.recurrence'].sudo().search([('base_event_id', 'in', self.calendar_event_ids.mapped('id'))])
        self.calendar_event_ids.unlink()
        if recurrence:
            recurrence.mapped('calendar_event_ids').unlink()
        return super(WedSchedule, self).unlink()


class ThuSchedule(models.Model):
    _name = 'group.thu.schedule'

    name = fields.Char(string="Training Name")
    thu_from = fields.Float(string="From")
    thu_to = fields.Float(string="To")
    venue_id = fields.Many2one('organisation.venues')
    is_recurrent = fields.Boolean(string="Recurrent")
    is_cancel = fields.Boolean(string="Is Cancelled?")
    group_id = fields.Many2one('athlete.groups')
    calendar_event_ids = fields.Many2many('calendar.event')

    def create(self, vals):
        res = super(ThuSchedule, self).create(vals)
        for rec in res:
            partner_ids = []
            athlete_partners = rec.group_id.athlete_ids.mapped('partner_id').ids
            coach_partners = rec.group_id.coach_ids.mapped('partner_id').ids
            group_coach = rec.group_id.coach_ids.mapped('id')[0]
            for athlete_partner in athlete_partners:
                partner_ids.append(athlete_partner)
            for coach in coach_partners:
                partner_ids.append(coach)
            weekday = 3  ## Thursday
            dt = datetime.now().replace(hour=0, minute=0,
                                                 second=0,microsecond=0)  ## or any specific date
            days_remaining = (weekday - dt.weekday() - 1) % 7 + 1
            next_dt = dt + timedelta(days_remaining)
            time_from = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.thu_from * 60, 60))
            time_to = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.thu_to * 60, 60))
            next_dt_str = next_dt.strftime('%Y-%m-%d')
            str_datetime_start = next_dt_str + ' ' + time_from
            str_datetime_end = next_dt_str + ' ' + time_to
            datetime_object = datetime.strptime(str_datetime_start, "%Y-%m-%d %H:%M")
            datetime_object_to = datetime.strptime(str_datetime_end, "%Y-%m-%d %H:%M")
            str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
            utc_offset = datetime.now(
                pytz.timezone(self.env.user.tz)).utcoffset().total_seconds()
            hour_utc_offset = utc_offset / 3600
            start = datetime_object + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            stop = datetime_object_to + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            event = self.env['calendar.event'].sudo().create({
                'name': '%s/%s' % (rec.group_id.name,
                                         rec.name,
                                        ),
                'start': start,
                'stop': stop,
                'recurrency': rec.is_recurrent,
                'interval': 1,
                'rrule_type': 'weekly',
                'thu': True,
                'end_type': 'forever',
                'group_id': rec.group_id.id,
                'group_coach_id': group_coach,
                # 'duration': duration,
                # 'has_booking': True,
                'venue_id': rec.venue_id.id if rec.venue_id.id else rec.group_id.venue_id.id,
                # 'coach_id': appointment_type.coach_id.id,
                # 'user_id': booking_coach_user.id,
                'is_web_create': True,
                'partner_ids': [[6, False, partner_ids]],
            })
            print(event, "event")
            rec.calendar_event_ids = [(4, event.id)]
        return res

    def unlink(self):
        recurrence = self.env['calendar.recurrence'].sudo().search([('base_event_id', 'in', self.calendar_event_ids.mapped('id'))])
        self.calendar_event_ids.unlink()
        if recurrence:
            recurrence.mapped('calendar_event_ids').unlink()
        return super(ThuSchedule, self).unlink()


class FriSchedule(models.Model):
    _name = 'group.fri.schedule'

    name = fields.Char(string="Training Name")
    fri_from = fields.Float(string="From")
    fri_to = fields.Float(string="To")
    venue_id = fields.Many2one('organisation.venues')
    is_recurrent = fields.Boolean(string="Recurrent")
    is_cancel = fields.Boolean(string="Is Cancelled?")
    group_id = fields.Many2one('athlete.groups')
    calendar_event_ids = fields.Many2many('calendar.event')

    def create(self, vals):
        res = super(FriSchedule, self).create(vals)
        for rec in res:
            partner_ids = []
            athlete_partners = rec.group_id.athlete_ids.mapped('partner_id').ids
            coach_partners = rec.group_id.coach_ids.mapped('partner_id').ids
            group_coach = rec.group_id.coach_ids.mapped('id')[0]
            for athlete_partner in athlete_partners:
                partner_ids.append(athlete_partner)
            for coach in coach_partners:
                partner_ids.append(coach)
            weekday = 4  ## Friday
            dt = datetime.now().replace(hour=0, minute=0,
                                                 second=0,microsecond=0)  ## or any specific date
            days_remaining = (weekday - dt.weekday() - 1) % 7 + 1
            next_dt = dt + timedelta(days_remaining)
            time_from = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.fri_from * 60, 60))
            time_to = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.fri_to * 60, 60))
            next_dt_str = next_dt.strftime('%Y-%m-%d')
            str_datetime_start = next_dt_str + ' ' + time_from
            str_datetime_end = next_dt_str + ' ' + time_to
            datetime_object = datetime.strptime(str_datetime_start, "%Y-%m-%d %H:%M")
            datetime_object_to = datetime.strptime(str_datetime_end, "%Y-%m-%d %H:%M")
            str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
            utc_offset = datetime.now(
                pytz.timezone(self.env.user.tz)).utcoffset().total_seconds()
            hour_utc_offset = utc_offset / 3600
            start = datetime_object + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            stop = datetime_object_to + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            event = self.env['calendar.event'].sudo().create({

                'name': '%s/%s' % (rec.group_id.name,
                                         rec.name,
                                        ),
                'start': start,
                'stop': stop,
                'recurrency': rec.is_recurrent,
                'interval': 1,
                'rrule_type': 'weekly',
                'fri': True,
                'end_type': 'forever',
                'group_id': rec.group_id.id,
                'group_coach_id': group_coach,
                # 'duration': duration,
                # 'has_booking': True,
                'venue_id': rec.venue_id.id if rec.venue_id.id else rec.group_id.venue_id.id,
                # 'coach_id': appointment_type.coach_id.id,
                # 'user_id': booking_coach_user.id,
                'is_web_create': True,
                'partner_ids': [[6, False, partner_ids]],
            })
            rec.calendar_event_ids = [(4, event.id)]
        return res

    def unlink(self):
        recurrence = self.env['calendar.recurrence'].sudo().search([('base_event_id', 'in', self.calendar_event_ids.mapped('id'))])
        self.calendar_event_ids.unlink()
        if recurrence:
            recurrence.mapped('calendar_event_ids').unlink()
        return super(FriSchedule, self).unlink()


class SatSchedule(models.Model):
    _name = 'group.sat.schedule'

    name = fields.Char(string="Training Name")
    sat_from = fields.Float(string="From")
    sat_to = fields.Float(string="To")
    venue_id = fields.Many2one('organisation.venues')
    is_recurrent = fields.Boolean(string="Recurrent")
    is_cancel = fields.Boolean(string="Is Cancelled?")
    group_id = fields.Many2one('athlete.groups')
    calendar_event_ids = fields.Many2many('calendar.event')

    def create(self, vals):
        res = super(SatSchedule, self).create(vals)
        for rec in res:
            partner_ids = []
            athlete_partners = rec.group_id.athlete_ids.mapped('partner_id').ids
            coach_partners = rec.group_id.coach_ids.mapped('partner_id').ids
            group_coach = rec.group_id.coach_ids.mapped('id')[0]
            for athlete_partner in athlete_partners:
                partner_ids.append(athlete_partner)
            for coach in coach_partners:
                partner_ids.append(coach)
            weekday = 5  ## Saturday
            dt = datetime.now().replace(hour=0, minute=0,
                                                 second=0,microsecond=0)  ## or any specific date
            days_remaining = (weekday - dt.weekday() - 1) % 7 + 1
            next_dt = dt + timedelta(days_remaining)
            time_from = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.sat_from * 60, 60))
            time_to = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.sat_to * 60, 60))
            next_dt_str = next_dt.strftime('%Y-%m-%d')
            str_datetime_start = next_dt_str + ' ' + time_from
            str_datetime_end = next_dt_str + ' ' + time_to
            datetime_object = datetime.strptime(str_datetime_start, "%Y-%m-%d %H:%M")
            datetime_object_to = datetime.strptime(str_datetime_end, "%Y-%m-%d %H:%M")
            str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
            utc_offset = datetime.now(
                pytz.timezone(self.env.user.tz)).utcoffset().total_seconds()
            hour_utc_offset = utc_offset / 3600
            start = datetime_object + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            stop = datetime_object_to + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            event = self.env['calendar.event'].sudo().create({

                'name': '%s/%s' % (rec.group_id.name,
                                         rec.name,
                                        ),
                'start': start,
                'stop': stop,
                'recurrency': rec.is_recurrent,
                'interval': 1,
                'rrule_type': 'weekly',
                'sat': True,
                'end_type': 'forever',
                'group_id': rec.group_id.id,
                'group_coach_id': group_coach,
                # 'duration': duration,
                # 'has_booking': True,
                'venue_id': rec.venue_id.id if rec.venue_id.id else rec.group_id.venue_id.id,
                # 'coach_id': appointment_type.coach_id.id,
                # 'user_id': booking_coach_user.id,
                'is_web_create': True,
                'partner_ids': [[6, False, partner_ids]],
            })
            print(event, "event")
            rec.calendar_event_ids = [(4, event.id)]
        return res

    def unlink(self):
        recurrence = self.env['calendar.recurrence'].sudo().search([('base_event_id', 'in', self.calendar_event_ids.mapped('id'))])
        self.calendar_event_ids.unlink()
        if recurrence:
            recurrence.mapped('calendar_event_ids').unlink()
        return super(SatSchedule, self).unlink()


class SunSchedule(models.Model):
    _name = 'group.sun.schedule'

    name = fields.Char(string="Training Name")
    sun_from = fields.Float(string="From")
    sun_to = fields.Float(string="To")
    venue_id = fields.Many2one('organisation.venues')
    is_recurrent = fields.Boolean(string="Recurrent")
    is_cancel = fields.Boolean(string="Is Cancelled?")
    group_id = fields.Many2one('athlete.groups')
    calendar_event_ids = fields.Many2many('calendar.event')

    def create(self, vals):
        res = super(SunSchedule, self).create(vals)
        for rec in res:
            partner_ids = []
            athlete_partners = rec.group_id.athlete_ids.mapped('partner_id').ids
            coach_partners = rec.group_id.coach_ids.mapped('partner_id').ids
            group_coach = rec.group_id.coach_ids.mapped('id')[0]
            for athlete_partner in athlete_partners:
                partner_ids.append(athlete_partner)
            for coach in coach_partners:
                partner_ids.append(coach)
            weekday = 6  ## Sunday
            dt = datetime.now().replace(hour=0, minute=0,
                                                 second=0,microsecond=0)  ## or any specific date
            days_remaining = (weekday - dt.weekday() - 1) % 7 + 1
            next_dt = dt + timedelta(days_remaining)
            time_from = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.sun_from * 60, 60))
            time_to = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.sun_to * 60, 60))
            next_dt_str = next_dt.strftime('%Y-%m-%d')
            str_datetime_start = next_dt_str + ' ' + time_from
            str_datetime_end = next_dt_str + ' ' + time_to
            datetime_object = datetime.strptime(str_datetime_start, "%Y-%m-%d %H:%M")
            datetime_object_to = datetime.strptime(str_datetime_end, "%Y-%m-%d %H:%M")
            str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
            utc_offset = datetime.now(
                pytz.timezone(self.env.user.tz)).utcoffset().total_seconds()
            hour_utc_offset = utc_offset / 3600
            start = datetime_object + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            stop = datetime_object_to + timedelta(
                minutes=round((-hour_utc_offset or -1.0) * 60))
            event = self.env['calendar.event'].sudo().create({

                'name': '%s/%s' % (rec.group_id.name,
                                         rec.name,
                                        ),
                'start': start,
                'stop': stop,
                'recurrency': rec.is_recurrent,
                'interval': 1,
                'rrule_type': 'weekly',
                'sun': True,
                'end_type': 'forever',
                'group_id': rec.group_id.id,
                'group_coach_id': group_coach,
                # 'duration': duration,
                # 'has_booking': True,
                'venue_id': rec.venue_id.id if rec.venue_id.id else rec.group_id.venue_id.id,
                # 'coach_id': appointment_type.coach_id.id,
                # 'user_id': booking_coach_user.id,
                'is_web_create': True,
                'partner_ids': [[6, False, partner_ids]],
            })
            rec.calendar_event_ids = [(4, event.id)]
        return res

    def unlink(self):
        recurrence = self.env['calendar.recurrence'].sudo().search([('base_event_id', 'in', self.calendar_event_ids.mapped('id'))])
        self.calendar_event_ids.unlink()
        if recurrence:
            recurrence.mapped('calendar_event_ids').unlink()
        return super(SunSchedule, self).unlink()