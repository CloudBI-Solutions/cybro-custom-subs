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


class BookingPortal(CustomerPortal):
    @http.route(['/my/bookings', '/my/bookings/page/<int:page>'], type='http', auth="user", website=True)
    def my_bookings(self, page=0, search='', **post):
        domain = []

        # org_domain = []
        # org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        # if request.httprequest.cookies.get('select_organisation') is not None:
        #     org_domain.append(('id', '=',
        #                        request.httprequest.cookies.get(
        #                            'select_organisation')))
        # organisation = request.env['organisation.organisation'].sudo().search(
        #     org_domain, limit=1)
        # if organisation:
        #     domain.append(('organisation_ids', 'in', [organisation.id]))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        bookings = request.env['booking.booking'].sudo().search(domain)
        # athletes = request.env['organisation.athletes'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        # parents = request.env['organisation.parents'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        # # coaches = request.env['organisation.coaches'].sudo().search(
        # #     [('organisation_ids', 'in', [organisation.id])])
        # groups = request.env['athlete.groups'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
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
            # 'athletes': athletes,
            # 'parents': parents,
            # 'groups': groups,
            # 'disciplines': disciplines,
            'pager': pager,
            'is_account': True,
            'total': total,
            # 'organisations': request.env[
            #     'organisation.organisation'].sudo().search(
            #     [('allowed_user_ids', 'in', [request.env.user.id])]),
            # 'total_coaches': coaches
        }
        return request.render('sports_erp_dashboard.booking_home_template', values)

    @http.route(['/my/booking/types', '/my/booking/types/page/<int:page>'], type='http',
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


        print("booking_types", booking_types.duration)


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
            request.env['booking.type'].sudo().browse(int(post.get('type'))).unlink()
        return request.redirect('/my/booking/types')
