from odoo import fields, _
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request, route
from datetime import datetime
import pytz
from datetime import timedelta


class CustomerPortalDashboard(CustomerPortal):

    def _coach_schedule_get_page_view_values(self, coach, access_token):
        values = {
            'coach': coach,
            'page_name': 'schedule_booking',
            'schedule': True
        }
        return self._get_page_view_values(coach, access_token, values,
                                          'schedule_booking', False)

    def _coach_create_schedule_get_page_view_values(self, coach, access_token):
        values = {
            'coach': coach,
            'page_name': 'create_booking_page',
            'create_schedule': True
        }
        return self._get_page_view_values(coach, access_token, values,
                                          'create_booking_page', False)

    def _coach_booking_get_page_view_values(self, coach, access_token):
        values = {
            'coach': coach,
            'page_name': 'coach_dashboard',
            'coach_booking_page': True
        }
        return self._get_page_view_values(coach, access_token, values,
                                          'my_dashboard_bookings', False)

    def _coach_athlete_booking_get_page_view_values(self, athlete,
                                                    access_token):
        values = {
            'athlete': athlete,
            'page_name': 'coach_athlete_list',
            'coach_athlete': True,
            'coach_athlete_booking': True,
        }
        return self._get_page_view_values(athlete, access_token, values,
                                          'coach_athlete_booking', False)

    def _parent_athlete_booking_get_page_view_values(self, athlete,
                                                     access_token):
        values = {
            'athlete': athlete,
            'page_name': 'parent_athlete_dashboard',
            'parent_athlete_booking': True,
        }
        return self._get_page_view_values(athlete, access_token, values,
                                          'parent_athlete_booking', False)

    @route(['/my/athlete-<int:athlete_id>/booking',
            '/athlete/athlete-<int:athlete_id>/booking',
            '/my/athlete-<int:athlete_id>/booking',
            '/athlete-<int:athlete_id>/booking'], type='http',
           auth='user',
           website=True)
    def dashboard_booking(self, athlete_id=None, access_token=None):
        athlete = request.env['organisation.athletes'].sudo().search(
            [('id', '=', athlete_id)])
        if not athlete:
            return request.redirect("/my")
        athlete_partner = athlete.partner_id
        athlete_user = request.env['res.users'].sudo().search([
            ('partner_id', '=', athlete_partner.id)
        ])
        bookings = athlete_partner.booking_ids
        user = request.env.user
        partner = user.partner_id
        my_bookings = request.env['booking.booking'].sudo().search(
            [('user_ids', 'in', athlete_user.id)])
        if partner.org_group_selection == 'ex_coaches':
            coach = request.env['organisation.coaches'].sudo().search([
                ('partner_id', '=', partner.id)
            ])
            coach_athletes = coach.athlete_ids
            if athlete.id not in coach_athletes.mapped('id'):
                return Forbidden()
            values = self._coach_athlete_booking_get_page_view_values(
                athlete, access_token)
        elif partner.org_group_selection == 'parents':
            parent = request.env['organisation.parents'].sudo().search([
                ('partner_id', '=', partner.id)
            ])
            parent_athletes = parent.athlete_ids
            if athlete.id not in parent_athletes.mapped('id'):
                return Forbidden()
            values = self._parent_athlete_booking_get_page_view_values(
                athlete, access_token)
        elif partner.org_group_selection == 'athletes':
            if athlete.partner_id != partner:
                return Forbidden()
                # raise NotFound()
            values = {}
        else:
            values = {}
        values.update({
            'athlete': athlete,
            'bookings': bookings,
            'partner': partner,
            'my_bookings': my_bookings,
        })
        response = request.render(
            "booking.portal_booking_dashboard", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/booking-<int:coach_id>'], type='http', auth='user',
           website=True)
    def coach_booking(self, coach_id=None, access_token=None):
        coach = request.env['organisation.coaches'].sudo().search(
            [('id', '=', coach_id)])
        if not coach:
            return request.redirect("/my")
        user = request.env.user
        partner = user.partner_id
        if partner.org_group_selection != 'ex_coaches':
            return request.redirect("/my")
        if coach.partner_id != partner:
            return Forbidden()
        bookings = partner.booking_ids
        my_bookings = request.env['booking.booking'].sudo().search(
            [('user_ids', 'in', user.id)])
        values = self._coach_booking_get_page_view_values(coach, access_token)
        values.update({
            'coach': coach,
            'bookings': bookings,
            'partner': partner,
            'my_bookings': my_bookings,
        })
        response = request.render(
            "booking.portal_booking_dashboard", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/booking'], type='http', auth='user', website=True)
    def booking(self, **post):
        booking = request.env['booking.booking'].sudo().search(
            [('id', '=', post.get('booking_id'))])
        types = request.env['booking.type'].sudo().search([])
        partner = request.env.user.partner_id
        values = {}
        values.update({
            'partner': partner,
            'booking': booking,
            'types': types,
            'page_name': 'schedule_booking'
        })

        response = request.render(
            "booking.portal_booking_form", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/cancel_booking'], type='http', auth='user', website=True)
    def cancel_booking(self, **post):
        booking = request.env['booking.booking'].sudo().search(
            [('id', '=', post['booking_id'])])
        partner = request.env.user.partner_id
        values = {}
        values.update({
            'partner': partner,
            'booking': booking,
        })

        response = request.render(
            "booking.portal_cancel_form", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/cancel_appointment'], type='http', auth='user', website=True)
    def cancel_appointment(self, **post):
        booking = request.env['booking.booking'].sudo().search(
            [('id', '=', post['booking_id'])])
        event = booking.event_id
        event.sudo().unlink()
        stage = request.env['booking.stage'].sudo().search(
            [('name', 'ilike', 'Follow-up')])
        booking.sudo().write({
            'event_id': False,
            'stage_id': stage.id,
            'state': 'follow_up',
        })
        values = {}
        partner = request.env.user.partner_id
        coach = request.env['organisation.coaches'].sudo().search(
            [('partner_id', '=', partner.id)])
        if coach and booking.assigned_partner_id == coach.partner_id:
            values.update({
                'coach': coach,
            })
            response = request.render(
                "organisation.portal_coach_dashboard", values)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        else:
            return request.redirect('/my/home')

    @route(['/get_booking_values'], type='json', auth='user', website=True)
    def get_booking_values(self, **post):
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

    @route(['/create_booking'], type='http', auth='user', website=True)
    def create_booking(self, **post):
        values = {}
        partner = request.env.user.partner_id
        if partner.org_group_selection == 'ex_coaches':
            coach = request.env['organisation.coaches'].sudo().search(
               [('partner_id', '=', partner.id)])
            values.update({
                'coach': coach,
            })
        if partner.org_group_selection == 'athletes':
            athlete = request.env['organisation.athletes'].sudo().search(
               [('partner_id', '=', partner.id)])
            values.update({
                'athlete': athlete,
            })
        if partner.org_group_selection == 'fans':
            fan = request.env['organisation.fans'].sudo().search(
               [('partner_id', '=', partner.id)])
            values.update({
                'fan': fan,
            })
        venues = request.env['organisation.venues'].sudo().search([])
        coaches = request.env['organisation.coaches'].sudo().search([])
        types = request.env['booking.type'].sudo().search([])
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        user_ids = request.env['res.users'].sudo().search(
            [('partner_id.organisation_ids', 'in', [organisation.id])])
        values.update({
            'venues': venues,
            'coaches': coaches,
            'types': types,
            'date': fields.Date.today(),
            'page_name': 'create_booking_page',
            # 'user_ids': user_ids
        })
        response = request.render(
            "booking.portal_create_booking_form", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/form_submit'], type='http', auth='user', website=True)
    def form_submit_booking(self, **post):
        print(post, "////////////")
        if 'slot' in post:
            today = fields.Datetime.now()
            user = request.env.user
            partner = user.partner_id
            appointment_type = request.env['booking.type'].sudo().search(
                [('id', '=', post['type_id'])])
            duration = appointment_type.duration
            partner_ids = []
            booking_coach = appointment_type.coach_id
            booking_coach_partner = request.env['res.partner'].sudo().search(
                [('id', '=', booking_coach.partner_id.id)])
            booking_coach_user = request.env['res.users'].sudo().search(
                [('partner_id', '=', booking_coach_partner.id)])
            partner_ids.append(booking_coach_partner.id)
            time = float(post['slot'])
            hours = int(time)
            minutes = (time * 60) % 60
            slot = " %d:%02d" % (hours, minutes)
            str_datetime = post['appointment_date'] + slot
            if 'assign_coach_id' in post:
                assign_coach = request.env['organisation.coaches'].sudo().search(
                   [('id', '=', post['assign_coach_id'])])
                assign_coach_user = request.env['res.users'].sudo().search(
                   [('partner_id', '=', assign_coach.partner_id.id)])
                booking = request.env['booking.booking'].sudo().create({
                    'date': fields.Date.today(),
                    'appointment_type_id': appointment_type.id,
                    'assigned_user_id': assign_coach_user.id,
                })
                partner_ids.append(assign_coach.partner_id.id)
                datetime_object = datetime.strptime(str_datetime, "%Y-%m-%d %H:%M")
                str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
                utc_offset = datetime.now(
                    pytz.timezone(user.tz)).utcoffset().total_seconds()
                hour_utc_offset = utc_offset / 3600
                start = datetime_object + timedelta(
                    minutes=round((-hour_utc_offset or -1.0) * 60))
                stop = start + timedelta(
                    minutes=round((duration or 1.0) * 60))
                event = request.env['calendar.event'].sudo().create({
                    'name': '%s/%s/%s/%s' % (appointment_type.name,
                                             appointment_type.venue_id.name,
                                             assign_coach_user.name,
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
                if event:
                    return request.render(
                        "booking.booking_creation_thanks_page")
                else:
                    return request.redirect('/my/home')
            elif 'assign_athlete_id' in post:
                assign_athlete = request.env['organisation.athletes'].sudo().search(
                    [('id', '=', post['assign_athlete_id'])])
                athlete_user = request.env['res.users'].sudo().search(
                    [('partner_id', '=', assign_athlete.partner_id.id)])
                partner_ids.append(athlete_user.partner_id.id)
                booking = request.env['booking.booking'].sudo().create({
                    'date': fields.Date.today(),
                    'appointment_type_id': appointment_type.id,
                    'assigned_user_id': athlete_user.id,
                    'user_ids': [[6, 0, [request.env.user.id]]]
                })
                datetime_object = datetime.strptime(str_datetime, "%Y-%m-%d %H:%M")
                str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
                utc_offset = datetime.now(
                    pytz.timezone(user.tz)).utcoffset().total_seconds()
                hour_utc_offset = utc_offset / 3600
                start = datetime_object + timedelta(
                    minutes=round((-hour_utc_offset or -1.0) * 60))
                stop = start + timedelta(
                    minutes=round((duration or 1.0) * 60))
                event = request.env['calendar.event'].sudo().create({
                    'name': '%s/%s/%s/%s' % (appointment_type.name,
                                             appointment_type.venue_id.name,
                                             athlete_user.name,
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
                if event:
                    return request.render(
                        "booking.booking_creation_thanks_page")
                else:
                    return request.redirect('/my/home')
            elif 'assign_fan_id' in post:
                assign_fan = request.env['organisation.fans'].sudo().search(
                    [('id', '=', post['assign_fan_id'])])
                fan_user = request.env['res.users'].sudo().search(
                    [('partner_id', '=', assign_fan.partner_id.id)])
                partner_ids.append(fan_user.partner_id.id)
                booking = request.env['booking.booking'].sudo().create({
                    'date': fields.Date.today(),
                    'appointment_type_id': appointment_type.id,
                    'assigned_user_id': fan_user.id,
                })
                datetime_object = datetime.strptime(str_datetime, "%Y-%m-%d %H:%M")
                str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
                utc_offset = datetime.now(
                    pytz.timezone(user.tz)).utcoffset().total_seconds()
                hour_utc_offset = utc_offset / 3600
                start = datetime_object + timedelta(
                    minutes=round((-hour_utc_offset or -1.0) * 60))
                stop = start + timedelta(
                    minutes=round((duration or 1.0) * 60))
                event = request.env['calendar.event'].sudo().create({
                    'name': '%s/%s/%s/%s' % (appointment_type.name,
                                             appointment_type.venue_id.name,
                                             fan_user.name,
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
                if event:
                    return request.render(
                        "booking.booking_creation_thanks_page")
                else:
                    return request.redirect('/my/home')
            else:
                user_ids = list(
                    map(int, request.httprequest.form.getlist('user_ids')))
                partners = request.env['res.users'].sudo().browse(
                    user_ids).mapped('partner_id').ids
                for rec in partners:
                    partner_ids.append(rec)

                # values = {
                #     'appointment_type_id': int(
                #         post.get('booking_type')) if post.get(
                #         'booking_type') else None,
                #     'date': post.get('date'),
                #     'description': post.get('description'),
                #     'assigned_user_id': int(
                #         post.get('assigned_user_id')) if post.get(
                #         'assigned_user_id') else None,
                #     'user_id': int(post.get('responsible')) if post.get(
                #         'responsible') else None,
                #     'event_id': int(post.get('calendar_event')) if post.get(
                #         'calendar_event') else None,
                #     'user_ids': [(4, user) for user in user_ids],
                # }
                booking = request.env['booking.booking'].sudo().create({
                    'date': fields.Date.today(),
                    'appointment_type_id': appointment_type.id,
                    'description': post.get('description'),
                    'user_ids': [(4, user) for user in user_ids],
                })
                print(booking.read(), user_ids, "idsss")
                datetime_object = datetime.strptime(str_datetime,
                                                    "%Y-%m-%d %H:%M")
                str_datetime = datetime_object.strftime('%d/%m/%Y %I:%M %p')
                utc_offset = datetime.now(
                    pytz.timezone(user.tz)).utcoffset().total_seconds()
                hour_utc_offset = utc_offset / 3600
                start = datetime_object + timedelta(
                    minutes=round((-hour_utc_offset or -1.0) * 60))
                stop = start + timedelta(
                    minutes=round((duration or 1.0) * 60))
                print(start, stop, partner_ids, "//////////////////////")
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
                user_ids.append(booking.assigned_user_id.id)
                booking.sudo().write({
                    'event_id': event.id,
                    'stage_id': stage.id,
                    'state': 'booked',
                    'user_ids': [(4, user) for user in user_ids]
                })
                print(event, "event")
                if event:
                    return request.render(
                        "booking.booking_creation_thanks_page")
                else:
                    return request.redirect('/my/home')
        else:
            return request.redirect('/my/home')

    @route(['/my/fan_booking/<int:fan_id>', '/fan_booking/<int:fan_id>'],
           type='http', auth='user', website=True)
    def fan_dashboard_booking(self, fan_id=None, access_token=None):
        fan = request.env['organisation.fans'].sudo().search(
            [('id', '=', fan_id)])
        if not fan:
            return request.redirect("/my")
        user = request.env.user
        partner = user.partner_id
        if partner.org_group_selection != 'fans':
            return request.redirect("/my")
        if fan.partner_id != partner:
            return Forbidden()
        bookings = partner.booking_ids
        my_bookings = request.env['booking.booking'].sudo().search(
            [('user_ids', 'in', user.id)])
        values = {}
        values.update({
            'fan': fan,
            'bookings': bookings,
            'partner': partner,
            'my_bookings': my_bookings,
            'page_name': 'fan_dashboard',
            'fan_booking': True
        })
        response = request.render(
            "booking.portal_booking_dashboard", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/get_coach_schedule'], type='json', auth='user', website=True)
    def get_coach_schedule(self, **post):
        user = request.env.user
        date = datetime.strptime(post['date'], '%Y-%m-%d')
        coach_id = str(post['coach_id'])
        type_id = str(post['type_id'])
        day = date.strftime("%A")
        coach = request.env['organisation.coaches'].sudo().search(
            [('id', '=', coach_id)])
        appointment_type = request.env['booking.type'].sudo().search(
            [('id', '=', type_id)])
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
                            pytz.timezone(user.tz)).utcoffset().total_seconds()
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
                            pytz.timezone(user.tz)).utcoffset().total_seconds()
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
                            pytz.timezone(user.tz)).utcoffset().total_seconds()
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
                            pytz.timezone(user.tz)).utcoffset().total_seconds()
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
                            pytz.timezone(user.tz)).utcoffset().total_seconds()
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
                            pytz.timezone(user.tz)).utcoffset().total_seconds()
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
                            pytz.timezone(user.tz)).utcoffset().total_seconds()
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
