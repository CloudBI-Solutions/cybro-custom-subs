
import json
from odoo import fields, _
import logging
from odoo import http
from odoo.http import request, route
from datetime import datetime
import pytz
from datetime import timedelta
from odoo.addons.website.controllers import form

_logger = logging.getLogger(__name__)


class BookingController(http.Controller):

    @route(['/public_booking'], type='http', auth='public', website=True)
    def create_public_booking(self):
        values = {}
        user = request.env.user
        venues = request.env['organisation.venues'].sudo().search([])
        coaches = request.env['organisation.coaches'].sudo().search([])
        types = request.env['booking.type'].sudo().search([])
        values.update({
            'user': user,
            'venues': venues,
            'coaches': coaches,
            'types': types,
            'date': fields.Date.today(),
            'page_name': 'create_public_booking_page',
        })
        response = request.render(
            "booking.portal_create_public_booking_form", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/get_public_booking_values'],
           type='json', auth='public', website=True)
    def get_public_booking_values(self, **post):
        type_id = post['type_id']
        appointment_type = request.env['booking.type'].sudo().search(
            [('id', '=', int(type_id))]
        )
        values = {}
        float_duration = appointment_type.duration
        hours = int(float_duration)
        minutes = (float_duration * 60) % 60
        values.update({
            'duration': "%d:%02d Hours" % (hours, minutes),
            'venue': appointment_type.venue_id.name,
            'coach': appointment_type.coach_id.name,

            'coach_id': appointment_type.coach_id.id,
        })
        return values

    @route(['/get_coach_schedule_public'],
           type='json', auth='public', website=True)
    def get_coach_schedule_public(self, **post):
        user = request.env.user
        tz = user.tz
        if not tz:
            tz = "Europe/Amsterdam"
        date = datetime.strptime(post['date'], '%Y-%m-%d')
        type_id = str(post['type_id'])
        day = date.strftime("%A")
        appointment_type = request.env['booking.type'].sudo().search(
            [('id', '=', type_id)])
        coach = appointment_type.coach_id
        params = request.env['ir.config_parameter'].sudo()
        conf_time_format = params.get_param('booking.time_format')
        schedule = []
        if day == 'Sunday':
            if coach.sun:
                sunday_slots = coach.sun_slot_ids
                for sunday_slot in sunday_slots:
                    time_from = sunday_slot.sun_from
                    time_to = sunday_slot.sun_to
                    duration = appointment_type.duration
                    slots = (time_to - time_from) / duration
                    time = time_from
                    for i in range(0, int(slots)):
                        hours = int(time)
                        minutes = (time * 60) % 60
                        slot = " %d:%02d:%02d" % (hours, minutes, 00)
                        str_datetime = date.strftime('%Y-%m-%d') + slot
                        obj_datetime = datetime.strptime(str_datetime,
                                                         "%Y-%m-%d %H:%M:%S")
                        utc_offset = datetime.now(
                            pytz.timezone(tz)).utcoffset().total_seconds()
                        hour_utc_offset = utc_offset / 3600
                        start = obj_datetime + timedelta(
                            minutes=round((-hour_utc_offset or -1.0) * 60))
                        event = request.env['calendar.event'].sudo().search([
                            ('start', '=', start)], limit=1)
                        if start > fields.Datetime.now() and not event:
                            if conf_time_format == "24_format":
                                schedule.append({
                                    'slot': "%d:%02d " % (hours, minutes),
                                    'time': time,
                                })
                            elif conf_time_format == "12_format":
                                str_time = "%d:%02d" % (hours, minutes)
                                for_time = datetime.strptime(str_time, "%H:%M")
                                schedule.append({
                                    'slot': for_time.strftime("%I:%M %p"),
                                    'time': time,
                                })
                            else:
                                schedule.append({
                                    'slot': "%d:%02d Hour" % (hours, minutes),
                                    'time': time,
                                })
                        time = time + duration
                return {'schedule': schedule}
            else:
                return {'schedule': schedule}
        elif day == 'Monday':
            if coach.mon:
                monday_slots = coach.mon_slot_ids
                for monday_slot in monday_slots:
                    time_from = monday_slot.mon_from
                    time_to = monday_slot.mon_to
                    duration = appointment_type.duration
                    slots = (time_to - time_from) / duration
                    time = time_from
                    for i in range(0, int(slots)):
                        hours = int(time)
                        minutes = (time * 60) % 60
                        slot = " %d:%02d:%02d" % (hours, minutes, 00)
                        str_datetime = date.strftime('%Y-%m-%d') + slot
                        obj_datetime = datetime.strptime(str_datetime,
                                                         "%Y-%m-%d %H:%M:%S")
                        utc_offset = datetime.now(
                            pytz.timezone(tz)).utcoffset().total_seconds()
                        hour_utc_offset = utc_offset / 3600
                        start = obj_datetime + timedelta(
                            minutes=round((-hour_utc_offset or -1.0) * 60))
                        event = request.env['calendar.event'].sudo().search([
                            ('start', '=', start)], limit=1)
                        if start > fields.Datetime.now() and not event:
                            if conf_time_format == "24_format":
                                schedule.append({
                                    'slot': "%d:%02d " % (hours, minutes),
                                    'time': time,
                                })
                            elif conf_time_format == "12_format":
                                str_time = "%d:%02d" % (hours, minutes)
                                for_time = datetime.strptime(str_time, "%H:%M")
                                schedule.append({
                                    'slot': for_time.strftime("%I:%M %p"),
                                    'time': time,
                                })
                            else:
                                schedule.append({
                                    'slot': "%d:%02d Hour" % (hours, minutes),
                                    'time': time,
                                })
                        time = time + duration
                return {'schedule': schedule}
            else:
                return {'schedule': schedule}
        elif day == 'Tuesday':
            if coach.tue:
                tuesday_slots = coach.tue_slot_ids
                for tuesday_slot in tuesday_slots:
                    time_from = tuesday_slot.tue_from
                    time_to = tuesday_slot.tue_to
                    duration = appointment_type.duration
                    slots = (time_to - time_from) / duration
                    time = time_from
                    for i in range(0, int(slots)):
                        hours = int(time)
                        minutes = (time * 60) % 60
                        slot = " %d:%02d:%02d" % (hours, minutes, 00)
                        str_datetime = date.strftime('%Y-%m-%d') + slot
                        obj_datetime = datetime.strptime(str_datetime,
                                                         "%Y-%m-%d %H:%M:%S")
                        utc_offset = datetime.now(
                            pytz.timezone(tz)).utcoffset().total_seconds()
                        hour_utc_offset = utc_offset / 3600
                        start = obj_datetime + timedelta(
                            minutes=round((-hour_utc_offset or -1.0) * 60))
                        event = request.env['calendar.event'].sudo().search([
                            ('start', '=', start)], limit=1)
                        if start > fields.Datetime.now() and not event:
                            if conf_time_format == "24_format":
                                schedule.append({
                                    'slot': "%d:%02d " % (hours, minutes),
                                    'time': time,
                                })
                            elif conf_time_format == "12_format":
                                str_time = "%d:%02d" % (hours, minutes)
                                for_time = datetime.strptime(str_time, "%H:%M")
                                schedule.append({
                                    'slot': for_time.strftime("%I:%M %p"),
                                    'time': time,
                                })
                            else:
                                schedule.append({
                                    'slot': "%d:%02d Hour" % (hours, minutes),
                                    'time': time,
                                })
                        time = time + duration
                return {'schedule': schedule}
            else:
                return {'schedule': schedule}
        elif day == 'Wednesday':
            if coach.wed:
                wednesday_slots = coach.wed_slot_ids
                for wednesday_slot in wednesday_slots:
                    time_from = wednesday_slot.wed_from
                    time_to = wednesday_slot.wed_to
                    duration = appointment_type.duration
                    slots = (time_to - time_from) / duration
                    time = time_from
                    for i in range(0, int(slots)):
                        hours = int(time)
                        minutes = (time * 60) % 60
                        slot = " %d:%02d:%02d" % (hours, minutes, 00)
                        str_datetime = date.strftime('%Y-%m-%d') + slot
                        obj_datetime = datetime.strptime(str_datetime,
                                                         "%Y-%m-%d %H:%M:%S")
                        utc_offset = datetime.now(
                            pytz.timezone(tz)).utcoffset().total_seconds()
                        hour_utc_offset = utc_offset / 3600
                        start = obj_datetime + timedelta(
                            minutes=round((-hour_utc_offset or -1.0) * 60))
                        event = request.env['calendar.event'].sudo().search([
                            ('start', '=', start)], limit=1)
                        if start > fields.Datetime.now() and not event:
                            if conf_time_format == "24_format":
                                schedule.append({
                                    'slot': "%d:%02d " % (hours, minutes),
                                    'time': time,
                                })
                            elif conf_time_format == "12_format":
                                str_time = "%d:%02d" % (hours, minutes)
                                for_time = datetime.strptime(str_time, "%H:%M")
                                schedule.append({
                                    'slot': for_time.strftime("%I:%M %p"),
                                    'time': time,
                                })
                            else:
                                schedule.append({
                                    'slot': "%d:%02d Hour" % (hours, minutes),
                                    'time': time,
                                })
                        time = time + duration
                return {'schedule': schedule}
            else:
                return {'schedule': schedule}
        elif day == 'Thursday':
            if coach.thu:
                thursday_slots = coach.thu_slot_ids
                for thursday_slot in thursday_slots:
                    time_from = thursday_slot.thu_from
                    time_to = thursday_slot.thu_to
                    duration = appointment_type.duration
                    slots = (time_to - time_from) / duration
                    time = time_from
                    for i in range(0, int(slots)):
                        hours = int(time)
                        minutes = (time * 60) % 60
                        slot = " %d:%02d:%02d" % (hours, minutes, 00)
                        str_datetime = date.strftime('%Y-%m-%d') + slot
                        obj_datetime = datetime.strptime(str_datetime,
                                                         "%Y-%m-%d %H:%M:%S")
                        utc_offset = datetime.now(
                            pytz.timezone(tz)).utcoffset().total_seconds()
                        hour_utc_offset = utc_offset / 3600
                        start = obj_datetime + timedelta(
                            minutes=round((-hour_utc_offset or -1.0) * 60))
                        event = request.env['calendar.event'].sudo().search([
                            ('start', '=', start)], limit=1)
                        if start > fields.Datetime.now() and not event:
                            if conf_time_format == "24_format":
                                schedule.append({
                                    'slot': "%d:%02d " % (hours, minutes),
                                    'time': time,
                                })
                            elif conf_time_format == "12_format":
                                str_time = "%d:%02d" % (hours, minutes)
                                for_time = datetime.strptime(str_time, "%H:%M")
                                schedule.append({
                                    'slot': for_time.strftime("%I:%M %p"),
                                    'time': time,
                                })
                            else:
                                schedule.append({
                                    'slot': "%d:%02d Hour" % (hours, minutes),
                                    'time': time,
                                })
                        time = time + duration
                return {'schedule': schedule}
            else:
                return {'schedule': schedule}
        elif day == 'Friday':
            if coach.fri:
                friday_slots = coach.fri_slot_ids
                for friday_slot in friday_slots:
                    time_from = friday_slot.fri_from
                    time_to = friday_slot.fri_to
                    duration = appointment_type.duration
                    slots = (time_to - time_from) / duration
                    time = time_from
                    for i in range(0, int(slots)):
                        hours = int(time)
                        minutes = (time * 60) % 60
                        slot = " %d:%02d:%02d" % (hours, minutes, 00)
                        str_datetime = date.strftime('%Y-%m-%d') + slot
                        obj_datetime = datetime.strptime(str_datetime,
                                                         "%Y-%m-%d %H:%M:%S")
                        utc_offset = datetime.now(
                            pytz.timezone(tz)).utcoffset().total_seconds()
                        hour_utc_offset = utc_offset / 3600
                        start = obj_datetime + timedelta(
                            minutes=round((-hour_utc_offset or -1.0) * 60))
                        event = request.env['calendar.event'].sudo().search([
                            ('start', '=', start)], limit=1)
                        if start > fields.Datetime.now() and not event:
                            if conf_time_format == "24_format":
                                schedule.append({
                                    'slot': "%d:%02d " % (hours, minutes),
                                    'time': time,
                                })
                            elif conf_time_format == "12_format":
                                str_time = "%d:%02d" % (hours, minutes)
                                for_time = datetime.strptime(str_time, "%H:%M")
                                schedule.append({
                                    'slot': for_time.strftime("%I:%M %p"),
                                    'time': time,
                                })
                            else:
                                schedule.append({
                                    'slot': "%d:%02d Hour" % (hours, minutes),
                                    'time': time,
                                })
                        time = time + duration
                return {'schedule': schedule}
            else:
                return {'schedule': schedule}
        elif day == 'Saturday':
            if coach.sat:
                saturday_slots = coach.sat_slot_ids
                for saturday_slot in saturday_slots:
                    time_from = saturday_slot.sat_from
                    time_to = saturday_slot.sat_to
                    duration = appointment_type.duration
                    slots = (time_to - time_from) / duration
                    time = time_from
                    for i in range(0, int(slots)):
                        hours = int(time)
                        minutes = (time * 60) % 60
                        slot = " %d:%02d:%02d" % (hours, minutes, 00)
                        str_datetime = date.strftime('%Y-%m-%d') + slot
                        obj_datetime = datetime.strptime(str_datetime,
                                                         "%Y-%m-%d %H:%M:%S")
                        utc_offset = datetime.now(
                            pytz.timezone(tz)).utcoffset().total_seconds()
                        hour_utc_offset = utc_offset / 3600
                        start = obj_datetime + timedelta(
                            minutes=round((-hour_utc_offset or -1.0) * 60))
                        event = request.env['calendar.event'].sudo().search([
                            ('start', '=', start)], limit=1)
                        if start > fields.Datetime.now() and not event:
                            if conf_time_format == "24_format":
                                schedule.append({
                                    'slot': "%d:%02d " % (hours, minutes),
                                    'time': time,
                                })
                            elif conf_time_format == "12_format":
                                str_time = "%d:%02d" % (hours, minutes)
                                for_time = datetime.strptime(str_time, "%H:%M")
                                schedule.append({
                                    'slot': for_time.strftime("%I:%M %p"),
                                    'time': time,
                                })
                            else:
                                schedule.append({
                                    'slot': "%d:%02d Hour" % (hours, minutes),
                                    'time': time,
                                })
                        time = time + duration
                return {'schedule': schedule}
            else:
                return {'schedule': schedule}
        else:
            return

    def _default_user_ids(self, partner_id):
        """methode to grant portal access"""
        welcome_message = ""
        contact_ids = set()
        user_changes = []
        partner = request.env['res.partner'].sudo().browse(partner_id)
        contact_partners = partner.child_ids.filtered(lambda p: p.type in ('contact', 'other')) | partner
        wizard_id = request.env['portal.wizard'].sudo().create(
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

    @route(['/create_public_booking'],
           type='http', auth='public', website=True)
    def public_booking(self, **post):
        request.session.update(post)
        access_form = False
        admin = request.env.ref('base.user_admin')
        web_user = request.env.user
        if 'public_slot' in post:
            access_form = True
            booking = True
            appointment_type = request.env['booking.type'].sudo().search(
                [('id', '=', post['type_id'])])
            time = float(post['public_slot'])
            hours = int(time)
            minutes = (time * 60) % 60
            slot = " %d:%02d" % (hours, minutes)
            str_datetime = post['appointment_date'] + slot
            # user_name = post['user_name']
            # user_email = post['user_email']
            # partner = request.env['res.partner'].sudo().create({
            #     'name': user_name,
            #     'email': user_email,
            #     'create_booking': True
            # })
            # fan = request.env['organisation.fans'].sudo().create({
            #     'partner_id': partner.id,
            # })
            # user_ids = request.env['portal.wizard.user'].sudo().create(
            #     self._default_user_ids(partner.id))
            # user_ids.action_apply()
            # user = request.env['res.users'].sudo().search([
            #     ('partner_id', '=', partner.id)
            # ])
            # tz = user.tz
            # if not tz:
            #     tz = "Europe/Amsterdam"
            # appointment_type = request.env['booking.type'].sudo().search(
            #     [('id', '=', post['type_id'])])
            # duration = appointment_type.duration
            # partner_ids = []
            # booking_coach = appointment_type.coach_id
            # booking_coach_partner = request.env['res.partner'].sudo().search(
            #     [('id', '=', booking_coach.partner_id.id)])
            # booking_coach_user = request.env['res.users'].sudo().search(
            #     [('partner_id', '=', booking_coach_partner.id)])
            # partner_ids.append(booking_coach_partner.id)
            # partner_ids.append(partner.id)
            # time = float(post['public_slot'])
            # hours = int(time)
            # minutes = (time * 60) % 60
            # slot = " %d:%02d" % (hours, minutes)
            # str_datetime = post['appointment_date'] + slot
            # booking = request.env['booking.booking'].sudo().create({
            #     'date': fields.Date.today(),
            #     'appointment_type_id': appointment_type.id,
            #     'assigned_user_id': user.id,
            #     'user_id': user.id
            # })
            # datetime_object = datetime.strptime(str_datetime, "%Y-%m-%d %H:%M")
            # str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
            # utc_offset = datetime.now(
            #     pytz.timezone(tz)).utcoffset().total_seconds()
            # hour_utc_offset = utc_offset / 3600
            # start = datetime_object + timedelta(
            #     minutes=round((-hour_utc_offset or -1.0) * 60))
            # stop = start + timedelta(
            #     minutes=round((duration or 1.0) * 60))
            # event = request.env['calendar.event'].sudo().create({
            #     'name': '%s/%s/%s' % (appointment_type.name,
            #                           appointment_type.venue_id.name,
            #                           str_datetime),
            #     'start': start,
            #     'stop': stop,
            #     'duration': duration,
            #     'has_booking': True,
            #     'booking_id': booking.id,
            #     'venue_id': appointment_type.venue_id.id,
            #     'coach_id': appointment_type.coach_id.id,
            #     'user_id': booking_coach_user.id,
            #     'is_web_create': True,
            #     'partner_ids': [[6, False, partner_ids]],
            # })
            #
            # stage = request.env['booking.stage'].sudo().search(
            #     [('name', 'ilike', 'Booked')])
            # booking.sudo().write({
            #     'event_id': event.id,
            #     'stage_id': stage.id,
            #     'state': 'booked',
            # })
            values = {}
            # hours = int(duration)
            # minutes = (duration * 60) % 60
            values.update({
                'user_name': post['user_name'],
                'user_email': post['user_email'],
                'appointment_type': appointment_type,
                'duration': " %d:%02d Hours" % (hours, minutes),
                'slot': str_datetime,
                'access_form': access_form,
                'booking': booking
            })
            return request.render(
                "booking.portal_confirm_public_booking_form", values)
        elif admin.id == web_user.id:
            access_form = True
            values = {}
            values.update({
                'booking': False,
                'access_form': access_form
            })
            return request.render(
                "booking.portal_confirm_public_booking_form", values)
        else:
            return request.redirect("/")


class WebsiteUserForm(form.WebsiteForm):

    def _default_user_ids(self, partner_id):
        """methode to grant portal access"""
        welcome_message = ""
        contact_ids = set()
        user_changes = []
        partner = request.env['res.partner'].sudo().browse(partner_id)
        contact_partners = partner.child_ids.filtered(lambda p: p.type in ('contact', 'other')) | partner
        wizard_id = request.env['portal.wizard'].sudo().create(
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

    def insert_record(self, request, model, values, custom, meta=None):
        is_user_model = model.model == 'res.users'
        if is_user_model:
            if 'public_slot' in request.session:
                user_name = request.session['user_name']
                user_email = request.session['user_email']
                partner = request.env['res.partner'].sudo().create({
                    'name': user_name,
                    'email': user_email,
                    'create_booking': True
                })
                fan = request.env['organisation.fans'].sudo().create({
                    'partner_id': partner.id,
                })
                user_ids = request.env['portal.wizard.user'].sudo().create(
                    self._default_user_ids(partner.id))
                user_ids.action_apply()
                user = request.env['res.users'].sudo().search([
                    ('partner_id', '=', partner.id)
                ])
                tz = user.tz
                if not tz:
                    tz = "Europe/Amsterdam"
                appointment_type = request.env['booking.type'].sudo().search(
                    [('id', '=', request.session['type_id'])])
                duration = appointment_type.duration
                partner_ids = []
                booking_coach = appointment_type.coach_id
                booking_coach_partner = request.env['res.partner'].sudo().search(
                    [('id', '=', booking_coach.partner_id.id)])
                booking_coach_user = request.env['res.users'].sudo().search(
                    [('partner_id', '=', booking_coach_partner.id)])
                partner_ids.append(booking_coach_partner.id)
                partner_ids.append(partner.id)
                time = float(request.session['public_slot'])
                hours = int(time)
                minutes = (time * 60) % 60
                slot = " %d:%02d" % (hours, minutes)
                str_datetime = request.session['appointment_date'] + slot
                booking = request.env['booking.booking'].sudo().create({
                    'date': fields.Date.today(),
                    'appointment_type_id': appointment_type.id,
                    'assigned_user_id': user.id,
                    'user_id': user.id
                })
                datetime_object = datetime.strptime(str_datetime, "%Y-%m-%d %H:%M")
                str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
                utc_offset = datetime.now(
                    pytz.timezone(tz)).utcoffset().total_seconds()
                hour_utc_offset = utc_offset / 3600
                start = datetime_object + timedelta(
                    minutes=round((-hour_utc_offset or -1.0) * 60))
                stop = start + timedelta(
                    minutes=round((duration or 1.0) * 60))
                event = request.env['calendar.event'].sudo().create({
                    'name': '%s/%s/%s' % (appointment_type.name,
                                          appointment_type.venue_id.name,
                                          str_datetime),
                    'start': start,
                    'stop': stop,
                    'duration': duration,
                    'has_booking': True,
                    'booking_id': booking.id,
                    'venue_id': appointment_type.venue_id.id,
                    'coach_id': appointment_type.coach_id.id,
                    'user_id': booking_coach_user.id,
                    'is_web_create': True,
                    'partner_ids': [[6, False, partner_ids]],
                })

                stage = request.env['booking.stage'].sudo().search(
                    [('name', 'ilike', 'Booked')])
                booking.sudo().write({
                    'event_id': event.id,
                    'stage_id': stage.id,
                    'state': 'booked',
                })
                user = request.env['res.users'].sudo().search(
                            [('partner_id', '=', partner.id)], limit=1)
                user.sudo().write(values)
        # result = super(WebsiteUserForm, self).insert_record(
        #     request, model, values, custom, meta=meta)
        # if is_user_model:
        #     user = request.env['res.users'].sudo().search(
        #         [('id', '=', result)]
        #     )
        #     booking = request.env['booking.booking'].sudo().search(
        #         [], limit=1, order='id desc')
        #     booking.sudo().write({
        #         'assigned_user_id': result,
        #         'user_id': result
        #     })
        #
                return user.id
