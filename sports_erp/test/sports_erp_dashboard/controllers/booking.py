import base64
import json

from odoo.addons.http_routing.models.ir_http import slug
from odoo import fields, _
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager
from collections import OrderedDict
from odoo.http import request, route
from datetime import datetime, date
from odoo.addons.website_sale.controllers.main import WebsiteSale
from dateutil.relativedelta import relativedelta
import pytz
from datetime import timedelta


class BookingPortal(CustomerPortal):
    @http.route(
        ['/bookings', '/bookings/page/<int:page>',], type='http', auth="public",
        website=True)
    def bookings(self, page=1, search=''):
        # if request.env.user._is_public():
        #     return request.redirect('/web/login')
        Bookings = request.env['product.template'].sudo().search([])
        products = request.env['product.product'].sudo().search([('is_booking', '=', True)])
        product_template = products.mapped('product_tmpl_id').ids
        print(product_template, "subscriptions")
        domain = [('id', 'in', product_template),
                  ('is_able_to_assign', '=', True), ('is_published', '=', True)]
        if search:
            domain.append(('name', 'ilike', search))
        bookings = Bookings.sudo().search(domain)
        print(bookings, "subscriptions")
        return request.render('sports_erp_dashboard.booking_portal_home_template',
                              {'bookings': bookings,
                               'is_account': True
                               })

    @http.route(['/my/bookings', '/my/bookings/page/<int:page>'], type='http',
                auth="user", website=True)
    def my_bookings(self, page=0, search='', **post):
        domain = []
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        if request.env.user.has_group(
                'organisation.group_organisation_coaches'):
            organisations = request.env['organisation.coaches'].sudo().search([
                ('partner_id', '=', request.env.user.partner_id.id)]).mapped('organisation_ids')
            org_domain.append(('id', 'in',
                               organisations.ids))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        if request.env.user.has_group('organisation.group_organisation_athletes'):
            athletes = request.env['organisation.athletes'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)]).mapped('partner_id')
            domain.append(('user_ids.partner_id', 'in', athletes.ids))
        elif request.env.user.has_group('organisation.group_organisation_parents'):
            athletes = request.env['organisation.parents'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)]).mapped('athlete_ids').mapped('partner_id')
            print(athletes, "athltes")
            domain.append(('user_ids.partner_id', 'in', athletes.ids))
        # if organisation:
        #     domain.append(('organisation_ids', 'in', [organisation.id]))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        bookings = request.env['booking.booking'].sudo().search(domain)
        booking_types = request.env['booking.type'].sudo().search(
            [])
        assigned_user_ids = request.env['res.users'].sudo().search(
            [('partner_id.org_group_selection', 'in',
              ['ex_coaches', 'parents', 'athletes', 'fans']),
             ('partner_id.organisation_ids', 'in', [organisation.id])])
        user_ids = request.env['res.users'].sudo().search(
            [('partner_id.organisation_ids', 'in', [organisation.id])])
        calendar_events = request.env['calendar.event'].sudo().search(
            [])
        # disciplines = request.env['organisation.discipline'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        total = len(bookings)
        pager = request.website.pager(
            url='/my/bookings',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        bookings = bookings[offset: offset + 5]
        values = {
            'search': search,
            'bookings': bookings,
            'booking_types': booking_types,
            'assigned_user_ids': assigned_user_ids,
            'user_ids': user_ids,
            'calendar_events': calendar_events,
            # 'athletes': athletes,
            # 'parents': parents,
            # 'groups': groups,
            # 'disciplines': disciplines,
            'pager': pager,
            'is_account': True,
            'total': total,
            'total_bookings': request.env[
                'booking.booking'].sudo().search(domain),
            # 'organisations': request.env[
            #     'organisation.organisation'].sudo().search(
            #     [('allowed_user_ids', 'in', [request.env.user.id])]),
            # 'total_coaches': coaches
        }
        return request.render('sports_erp_dashboard.booking_home_template',
                              values)

    @http.route(['/my/create/bookings'],
                type='http',
                auth="user", website=True)
    def my_create_booking(self, **post):
        print("POST", post)
        user_ids = list(
            map(int, request.httprequest.form.getlist('user_ids')))
        values = {
            'appointment_type_id': int(post.get('booking_type')) if post.get(
                'booking_type') else None,
            'date': post.get('date'),
            'description': post.get('description'),
            'assigned_user_id': int(post.get('assigned_user_id')) if post.get(
                'assigned_user_id') else None,
            'user_id': int(post.get('responsible')) if post.get(
                'responsible') else None,
            'event_id': int(post.get('calendar_event')) if post.get(
                'calendar_event') else None,
            'user_ids': [(4, user) for user in user_ids],
        }
        request.env['booking.booking'].sudo().create(values)
        return request.redirect('/my/bookings')

    @http.route(['/my/booking/edit'],
                type='http',
                auth="user", website=True)
    def edit_booking(self, **post):
        if post.get('booking'):
            print("pos", post.get('booking'))
            request.env['booking.booking'].sudo().browse(
                int(post.get('booking'))).unlink()
        return request.redirect('/my/bookings')

    @http.route(['/my/booking/delete'],
                type='http',
                auth="user", website=True)
    def delete_booking(self, **post):
        if post.get('booking'):
            print("pos", post.get('booking'))
            request.env['booking.booking'].sudo().browse(
                int(post.get('booking'))).unlink()
        return request.redirect('/my/bookings')

    @http.route(['/my/booking/types', '/my/booking/types/page/<int:page>'],
                type='http',
                auth="user", website=True)
    def my_booking_types(self, page=0, search='', **post):
        domain = []

        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        # if organisation:
        #     domain.append(('organisation_ids', 'in', [organisation.id]))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        booking_types = request.env['booking.type'].sudo().search(domain)

        # print("booking_types", booking_types.duration)

        # athletes = request.env['organisation.athletes'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        # parents = request.env['organisation.parents'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        coaches = request.env['organisation.coaches'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        venues = request.env['organisation.venues'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        # disciplines = request.env['organisation.discipline'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        total = len(booking_types)
        pager = request.website.pager(
            url='/my/booking/types',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        booking_types = booking_types[offset: offset + 5]
        values = {
            'search': search,
            'booking_types': booking_types,
            'venues': venues,
            'coaches': coaches,
            # 'parents': parents,
            # 'groups': groups,
            # 'disciplines': disciplines,
            'pager': pager,
            'is_account': True,
            'total': total,
            'total_booking_types': request.env[
                'booking.type'].sudo().search(domain)
            # 'organisations': request.env[
            #     'organisation.organisation'].sudo().search(
            #     [('allowed_user_ids', 'in', [request.env.user.id])]),
            # 'total_coaches': coaches
        }
        return request.render('sports_erp_dashboard.booking_types_template',
                              values)

    @http.route(['/create/booking/type'],
                type='http',
                auth="user", website=True)
    def create_booking_types(self, **post):

        values = {
            'name': post.get('name'),
            'duration': float(post.get('duration').replace(':', '.')),
            'description': post.get('description'),
            'coach_id': post.get('coach'),
            'venue_id': post.get('venue')
        }
        request.env['booking.type'].sudo().create(values)
        return request.redirect('/my/booking/types')

    @http.route(['/my/booking/type/delete'],
                type='http',
                auth="user", website=True)
    def delete_booking_types(self, **post):
        if post.get('type'):
            request.env['booking.type'].sudo().browse(
                int(post.get('type'))).unlink()
        return request.redirect('/my/booking/types')

    @http.route(['/my/coach/schedule', '/my/coach/schedule/page/<int:page>'],
                type='http',
                auth="user", website=True)
    def my_coach_schedule(self, page=0, search='', **post):
        domain = []

        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        coach_schedule = request.env['organisation.coaches'].sudo().search(
            domain)

        print("booking_types")

        # athletes = request.env['organisation.athletes'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        # parents = request.env['organisation.parents'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        coaches = request.env['organisation.coaches'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        venues = request.env['organisation.venues'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        # disciplines = request.env['organisation.discipline'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        total = len(coach_schedule)
        pager = request.website.pager(
            url='/my/booking/types',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        coach_schedule = coach_schedule[offset: offset + 5]
        values = {
            'search': search,
            'coach_schedule': coach_schedule,
            'venues': venues,
            'coaches': coaches,
            # 'parents': parents,
            # 'groups': groups,
            # 'disciplines': disciplines,
            'pager': pager,
            'is_account': True,
            'total': total,
            'total_coach_schedule': request.env[
                'organisation.coaches'].sudo().search(domain)
            # 'organisations': request.env[
            #     'organisation.organisation'].sudo().search(
            #     [('allowed_user_ids', 'in', [request.env.user.id])]),
            # 'total_coaches': coaches
        }
        return request.render('sports_erp_dashboard.coach_schedules_template',
                              values)

    @http.route(['/my/coach/schedule/edit'],
                type='http',
                auth="user", website=True)
    def edit_coach_schedule(self, **post):
        print(post, "post")
        if post.get('coach'):
            coach = request.env['organisation.coaches'].sudo().browse(
                int(post.get('coach')))
            return request.render('sports_erp_dashboard.coach_schedule_details',
                                  {'coach': coach, 'is_account': True})
        # if post.get('booking'):
        #     print("pos", post.get('booking'))
        #     request.env['booking.booking'].sudo().browse(
        #         int(post.get('booking'))).unlink()
        return request.redirect('/my/coach/schedule')

    @http.route(
        ['/my/calendar/checklist', '/my/calendar/checklist/page/<int:page>'],
        type='http',
        auth="user", website=True)
    def my_calendar_checklist(self, page=0, search='', **post):
        domain = []

        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        # if organisation:
        #     domain.append(('organisation_ids', 'in', [organisation.id]))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        calendar_checklist = request.env['calendar.checklist'].sudo().search(
            domain)

        print("booking_types", calendar_checklist)

        # athletes = request.env['organisation.athletes'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        # parents = request.env['organisation.parents'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        coaches = request.env['organisation.coaches'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        venues = request.env['organisation.venues'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        # disciplines = request.env['organisation.discipline'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        total = len(calendar_checklist)
        pager = request.website.pager(
            url='/my/calendar/checklist',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        calendar_checklist = calendar_checklist[offset: offset + 5]
        values = {
            'search': search,
            'calendar_checklist': calendar_checklist,
            'venues': venues,
            'coaches': coaches,
            # 'parents': parents,
            # 'groups': groups,
            # 'disciplines': disciplines,
            'pager': pager,
            'is_account': True,
            'total': total,
            'total_calendar_checklist': request.env['calendar.checklist'].sudo().search(
                domain),
            # 'organisations': request.env[
            #     'organisation.organisation'].sudo().search(
            #     [('allowed_user_ids', 'in', [request.env.user.id])]),
            # 'total_coaches': coaches
        }
        return request.render('sports_erp_dashboard.checkist_template',
                              values)

    @route(['/my/booking/form_submit'], type='http', auth='user', website=True)
    def submit_booking(self, **post):
        print(post, "////////////")
        if 'slot' in post:
            today = fields.Datetime.now()
            user = request.env.user
            partner = user.partner_id
            appointment_type = request.env['booking.type'].sudo().search(
                [('id', '=', post['booking_type'])])
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
            str_datetime = post['date'] + slot
            if 'assign_coach_id' in post:
                assign_coach = request.env[
                    'organisation.coaches'].sudo().search(
                    [('id', '=', post['assign_coach_id'])])
                assign_coach_user = request.env['res.users'].sudo().search(
                    [('partner_id', '=', assign_coach.partner_id.id)])
                booking = request.env['booking.booking'].sudo().create({
                    'date': fields.Date.today(),
                    'appointment_type_id': appointment_type.id,
                    'assigned_user_id': assign_coach_user.id,
                })
                partner_ids.append(assign_coach.partner_id.id)
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
                assign_athlete = request.env[
                    'organisation.athletes'].sudo().search(
                    [('id', '=', post['assign_athlete_id'])])
                athlete_user = request.env['res.users'].sudo().search(
                    [('partner_id', '=', assign_athlete.partner_id.id)])
                partner_ids.append(athlete_user.partner_id.id)
                booking = request.env['booking.booking'].sudo().create({
                    'date': fields.Date.today(),
                    'appointment_type_id': appointment_type.id,
                    'assigned_user_id': athlete_user.id,
                })
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
                    'assigned_user_id': int(
                        post.get('assigned_user_id')) if post.get(
                        'assigned_user_id') else None,
                    'user_id': int(post.get('responsible')) if post.get(
                        'responsible') else None,
                    'event_id': int(post.get('calendar_event')) if post.get(
                        'calendar_event') else None,
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

                booking.sudo().write({
                    'event_id': event.id,
                    'stage_id': stage.id,
                    'state': 'booked',
                })
                # if event:
                #     return request.render(
                #         "booking.booking_creation_thanks_page")
                # else:
                return request.redirect('/my/bookings')
        else:
            return request.redirect('/my/home')

    @route(['/update/coach/schedule'], type='http', auth='user', website=True)
    def update_coach_schedule(self, **post):
        print(post, "////////////")
        keys = post.keys()
        key_list = []
        for key in keys:
            if len(key.split('_')) > 1:
                key_list.append(key.split('_')[2])
        maximum = max(list(set(key_list)))
        minimum = min(list(set(key_list)))
        print(maximum, minimum)
        coach = request.env['organisation.coaches'].sudo().search(
            [('id', '=', post.get('coach'))])
        print(coach, "coach")
        coach.sudo().write({
            'mon': True if post.get('monday') == 'on' else False,
            'tue': True if post.get('tuesday') == 'on' else False,
            'wed': True if post.get('wednesday') == 'on' else False,
            'thu': True if post.get('thursday') == 'on' else False,
            'fri': True if post.get('friday') == 'on' else False,
            'sat': True if post.get('saturday') == 'on' else False,
            'sun': True if post.get('sunday') == 'on' else False,
            'mon_slot_ids': [(5, 0, 0)],
            'tue_slot_ids': [(5, 0, 0)],
            'wed_slot_ids': [(5, 0, 0)],
            'thu_slot_ids': [(5, 0, 0)],
            'fri_slot_ids': [(5, 0, 0)],
            'sat_slot_ids': [(5, 0, 0)],
            'sun_slot_ids': [(5, 0, 0)],
        })
        for i in range(int(minimum), int(maximum) + 1):
            if post.get('mon_from_' + str(i)) and post.get('mon_to_' + str(i)):
                request.env['slot.monday'].sudo().create({
                    'mon_from': post.get('mon_from_' + str(i)),
                    'mon_to': post.get('mon_to_' + str(i)),
                    'coach_id': post.get('coach')
                })
            if post.get('tue_from_' + str(i)) and post.get('tue_to_' + str(i)):
                request.env['slot.tuesday'].sudo().create({
                    'tue_from': post.get('tue_from_' + str(i)),
                    'tue_to': post.get('tue_to_' + str(i)),
                    'coach_id': post.get('coach')
                })
            if post.get('wed_from_' + str(i)) and post.get('wed_to_' + str(i)):
                request.env['slot.wednesday'].sudo().create({
                    'wed_from': post.get('wed_from_' + str(i)),
                    'wed_to': post.get('wed_to_' + str(i)),
                    'coach_id': post.get('coach')
                })
            if post.get('thu_from_' + str(i)) and post.get('thu_to_' + str(i)):
                request.env['slot.thursday'].sudo().create({
                    'thu_from': post.get('thu_from_' + str(i)),
                    'thu_to': post.get('thu_to_' + str(i)),
                    'coach_id': post.get('coach')
                })
            if post.get('fri_from_' + str(i)) and post.get('fri_to_' + str(i)):
                request.env['slot.friday'].sudo().create({
                    'fri_from': post.get('fri_from_' + str(i)),
                    'fri_to': post.get('fri_to_' + str(i)),
                    'coach_id': post.get('coach')
                })
            if post.get('sat_from_' + str(i)) and post.get('sat_to_' + str(i)):
                request.env['slot.saturday'].sudo().create({
                    'sat_from': post.get('sat_from_' + str(i)),
                    'sat_to': post.get('sat_to_' + str(i)),
                    'coach_id': post.get('coach')
                })
            if post.get('sun_from_' + str(i)) and post.get('sun_to_' + str(i)):
                request.env['slot.sunday'].sudo().create({
                    'sun_from': post.get('sun_from_' + str(i)),
                    'sun_to': post.get('sun_to_' + str(i)),
                    'coach_id': post.get('coach')
                })
        return request.redirect('/my/coach/schedule/edit?coach=%s' % coach.id)