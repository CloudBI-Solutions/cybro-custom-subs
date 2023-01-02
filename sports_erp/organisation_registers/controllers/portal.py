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
from odoo.addons.sports_erp_dashboard.controllers.portal import Organisation
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError
from odoo.osv import expression
import re
from dateutil.relativedelta import relativedelta


class OrganisationGroups(Organisation):
    @http.route('/update/group',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def update_group(self, **post):
        values = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone')
        }
        group = request.env['athlete.groups'].sudo().browse(
            int(post.get('group')))
        keys = post.keys()
        key_list = []
        for key in keys:
            if len(key.split('_')) > 1:
                key_list.append(key.split('_')[2])
        maximum = 1
        minimum = 1
        if key_list:
            str_list = [x for x in key_list if x != '']
            maximum = max(list(set(str_list)))
            minimum = min(list(set(str_list)))
        group.sudo().write({
            'mon': True if post.get('monday') == 'on' else False,
            'tue': True if post.get('tuesday') == 'on' else False,
            'wed': True if post.get('wednesday') == 'on' else False,
            'thu': True if post.get('thursday') == 'on' else False,
            'fri': True if post.get('friday') == 'on' else False,
            'sat': True if post.get('saturday') == 'on' else False,
            'sun': True if post.get('sunday') == 'on' else False,
        })

        for i in range(int(minimum), int(maximum) + 1):
            if post.get('mon_from_' + str(i)) and post.get('mon_to_' + str(i)):
                if post.get('mon_id_' + str(i)):
                    mon_schedule = request.env['group.mon.schedule'].sudo().browse(int(post.get('mon_id_' + str(i))))
                    if mon_schedule:
                        mon_schedule.sudo().write({
                            'name': post.get('mon_name_' + str(i)) if post.get(
                                'mon_name_' + str(i)) else mon_schedule.name,
                            'mon_from': float(
                                post.get('mon_from_' + str(i)).replace(":",
                                                                       ".")) if post.get(
                                'mon_from_' + str(i)) else mon_schedule.mon_from,
                            'mon_to': float(
                                post.get('mon_to_' + str(i)).replace(":", ".")) if post.get(
                                'mon_to_' + str(i)) else mon_schedule.mon_to,
                            'group_id': group.id,
                            'is_recurrent': post.get('mon_recurrent_' + str(i)) if post.get(
                                'mon_recurrent_' + str(i)) else mon_schedule.is_recurrent,
                            'venue_id': int(
                                post.get('mon_venue_' + str(i))) if post.get(
                                'mon_venue_' + str(i)) else mon_schedule.venue_id.id,
                        })
                else:
                    request.env['group.mon.schedule'].sudo().create({
                        'name': post.get('mon_name_' + str(i)),
                        'mon_from': float(post.get('mon_from_' + str(i)).replace(":",".")),
                        'mon_to': float(post.get('mon_to_' + str(i)).replace(":",".")),
                        'group_id': group.id,
                        'is_recurrent': post.get('mon_recurrent_' + str(i)),
                        'venue_id': int(post.get('mon_venue_' + str(i))) if post.get('mon_venue_' + str(i)) else False,
                    })
            if post.get('tue_from_' + str(i)) and post.get('tue_to_' + str(i)):
                if post.get('tue_id_' + str(i)):
                    tue_schedule = request.env['group.tue.schedule'].sudo().browse(int(post.get('tue_id_' + str(i))))
                    if tue_schedule:
                        tue_schedule.sudo().write({
                            'name': post.get('tue_name_' + str(i)) if post.get(
                                'tue_name_' + str(i)) else tue_schedule.name,
                            'tue_from': float(
                                post.get('tue_from_' + str(i)).replace(":",
                                                                       ".")) if post.get(
                                'tue_from_' + str(i)) else tue_schedule.tue_from,
                            'tue_to': float(
                                post.get('tue_to_' + str(i)).replace(":", ".")) if post.get(
                                'tue_to_' + str(i)) else tue_schedule.tue_to,
                            'group_id': group.id,
                            'is_recurrent': post.get('tue_recurrent_' + str(i)) if post.get(
                                'tue_recurrent_' + str(i)) else tue_schedule.is_recurrent,
                            'venue_id': int(
                                post.get('tue_venue_' + str(i))) if post.get(
                                'tue_venue_' + str(i)) else tue_schedule.venue_id.id,
                        })
                else:
                    request.env['group.tue.schedule'].sudo().create({
                        'name': post.get('tue_name_' + str(i)),
                        'tue_from': float(
                            post.get('tue_from_' + str(i)).replace(":", ".")),
                        'tue_to': float(
                            post.get('tue_to_' + str(i)).replace(":", ".")),
                        'group_id': group.id,
                        'is_recurrent': post.get('tue_recurrent_' + str(i)),
                        'venue_id': int(
                            post.get('tue_venue_' + str(i))) if post.get(
                            'tue_venue_' + str(i)) else False,
                    })

            if post.get('wed_from_' + str(i)) and post.get('wed_to_' + str(i)):
                if post.get('wed_id_' + str(i)):
                    wed_schedule = request.env['group.wed.schedule'].sudo().browse(int(post.get('wed_id_' + str(i))))
                    if wed_schedule:
                        wed_schedule.sudo().write({
                            'name': post.get('wed_name_' + str(i)) if post.get(
                                'wed_name_' + str(i)) else wed_schedule.name,
                            'wed_from': float(
                                post.get('wed_from_' + str(i)).replace(":", ".")) if post.get('wed_from_' + str(i)) else wed_schedule.wed_from,
                            'wed_to': float(
                                post.get('wed_to_' + str(i)).replace(":", ".")) if post.get('wed_to_' + str(i)) else wed_schedule.wed_to,
                            'group_id': group.id,
                            'is_recurrent': post.get('wed_recurrent_' + str(i)) if post.get('wed_recurrent_' + str(i)) else wed_schedule.is_recurrent,
                            'venue_id': int(
                                post.get('wed_venue_' + str(i))) if post.get(
                                'wed_venue_' + str(i)) else wed_schedule.venue_id.id,
                        })
                else:
                    request.env['group.wed.schedule'].sudo().create({
                        'name': post.get('wed_name_' + str(i)),
                        'wed_from': float(
                            post.get('wed_from_' + str(i)).replace(":",
                                                                   ".")),
                        'wed_to': float(
                            post.get('wed_to_' + str(i)).replace(":", ".")),
                        'group_id': group.id,
                        'is_recurrent': post.get('wed_recurrent_' + str(i)),
                        'venue_id': int(
                            post.get('wed_venue_' + str(i))) if post.get(
                            'wed_venue_' + str(i)) else False,
                    })
            if post.get('thu_from_' + str(i)) and post.get('thu_to_' + str(i)):
                if post.get('thu_id_' + str(i)):
                    thu_schedule = request.env['group.thu.schedule'].sudo().browse(int(post.get('thu_id_' + str(i))))
                    if thu_schedule:
                        thu_schedule.sudo().write({
                            'name': post.get('thu_name_' + str(i)) if post.get('thu_name_' + str(i)) else thu_schedule.name,
                            'thu_from': float(
                                post.get('thu_from_' + str(i)).replace(":", ".")) if post.get('thu_from_' + str(i)) else thu_schedule.thu_from,
                            'thu_to': float(
                                post.get('thu_to_' + str(i)).replace(":", ".")) if post.get('thu_to_' + str(i)) else thu_schedule.thu_to,
                            'group_id': group.id,
                            'is_recurrent': post.get('thu_recurrent_' + str(i)) if post.get('thu_recurrent_' + str(i)) else thu_schedule.is_recurrent,
                            'venue_id': int(
                                post.get('thu_venue_' + str(i))) if post.get(
                                'thu_venue_' + str(i)) else thu_schedule.venue_id.id,
                        })
                else:
                    request.env['group.thu.schedule'].sudo().create({
                        'name': post.get('thu_name_' + str(i)),
                        'thu_from': float(
                            post.get('thu_from_' + str(i)).replace(":",
                                                                   ".")),
                        'thu_to': float(
                            post.get('thu_to_' + str(i)).replace(":",
                                                                 ".")),
                        'group_id': group.id,
                        'is_recurrent': post.get(
                            'thu_recurrent_' + str(i)),
                        'venue_id': int(
                            post.get('thu_venue_' + str(i))),
                    })
            if post.get('fri_from_' + str(i)) and post.get('fri_to_' + str(i)):
                if post.get('fri_id_' + str(i)):
                    fri_schedule = request.env['group.fri.schedule'].sudo().browse(int(post.get('fri_id_' + str(i))))
                    if fri_schedule:
                        fri_schedule.sudo().write({
                            'name': post.get('fri_name_' + str(i)) if post.get('fri_name_' + str(i)) else fri_schedule.name,
                            'fri_from': float(
                                post.get('fri_from_' + str(i)).replace(":", ".")) if post.get('fri_from_' + str(i)) else fri_schedule.fri_from,
                            'fri_to': float(
                                post.get('fri_to_' + str(i)).replace(":", ".")) if post.get('fri_to_' + str(i)) else fri_schedule.fri_to,
                            'group_id': group.id,
                            'is_recurrent': post.get('fri_recurrent_' + str(i)) if post.get('fri_recurrent_' + str(i)) else fri_schedule.is_recurrent,
                            'venue_id': int(
                                post.get('fri_venue_' + str(i))) if post.get(
                                'fri_venue_' + str(i)) else fri_schedule.venue_id.id,
                        })
                else:
                    request.env['group.fri.schedule'].sudo().create({
                        'name': post.get('fri_name_' + str(i)),
                        'fri_from': float(
                            post.get('fri_from_' + str(i)).replace(":", ".")),
                        'fri_to': float(
                            post.get('fri_to_' + str(i)).replace(":", ".")),
                        'group_id': group.id,
                        'is_recurrent': post.get('fri_recurrent_' + str(i)),
                        'venue_id': int(
                            post.get('fri_venue_' + str(i))) if post.get(
                            'fri_venue_' + str(i)) else False,
                    })
            if post.get('sat_from_' + str(i)) and post.get('sat_to_' + str(i)):
                if post.get('sat_id_' + str(i)):
                    sat_schedule = request.env['group.sat.schedule'].sudo().browse(int(post.get('sat_id_' + str(i))))
                    if sat_schedule:
                        sat_schedule.sudo().write({
                            'name': post.get('sat_name_' + str(i)) if post.get('sat_name_' + str(i)) else sat_schedule.name,
                            'sat_from': float(
                        post.get('sat_from_' + str(i)).replace(":", ".")) if post.get('sat_from_' + str(i)) else sat_schedule.sat_from,
                            'sat_to': float(
                        post.get('sat_to_' + str(i)).replace(":", ".")) if post.get('sat_to_' + str(i)) else sat_schedule.sat_to,
                            'group_id': group.id,
                            'is_recurrent': post.get('sat_recurrent_' + str(i)) if post.get('sat_recurrent_' + str(i)) else sat_schedule.is_recurrent,
                            'venue_id': int(
                        post.get('sat_venue_' + str(i))) if post.get(
                        'sat_venue_' + str(i)) else sat_schedule.venue_id.id
                        })
                else:
                    request.env['group.sat.schedule'].sudo().create({
                    'name': post.get('sat_name_' + str(i)),
                    'sat_from': float(
                        post.get('sat_from_' + str(i)).replace(":", ".")),
                    'sat_to': float(
                        post.get('sat_to_' + str(i)).replace(":", ".")),
                    'group_id': group.id,
                    'is_recurrent': post.get('sat_recurrent_' + str(i)),
                    'venue_id': int(
                        post.get('sat_venue_' + str(i))) if post.get(
                        'sat_venue_' + str(i)) else False,
                })
            if post.get('sun_from_' + str(i)) and post.get('sun_to_' + str(i)):
                if post.get('sun_id_' + str(i)):
                    sun_schedule = request.env['group.sun.schedule'].sudo().browse(int(post.get('sun_id_' + str(i))))
                    if sun_schedule:
                        sun_schedule.sudo().write({
                            'name': post.get('sun_name_' + str(i)) if post.get('sun_name_' + str(i)) else sun_schedule.name,
                            'sun_from': float(post.get('sun_from_' + str(i)).replace(":", ".")) if post.get('sun_from_' + str(i)) else sun_schedule.sun_from,
                            'sun_to': float(
                                post.get('sun_to_' + str(i)).replace(":", ".")) if post.get('sun_to_' + str(i)) else sun_schedule.sun_to,
                            'group_id': group.id,
                            'is_recurrent': post.get('sun_recurrent_' + str(i)) if post.get('sun_recurrent_' + str(i)) else sun_schedule.is_recurrent,
                            'venue_id': int(
                                post.get('sun_venue_' + str(i))) if post.get(
                                'sun_venue_' + str(i)) else sun_schedule.venue_id.id,
                        })
                else:
                    request.env['group.sun.schedule'].sudo().create({
                        'name': post.get('sun_name_' + str(i)),
                        'sun_from': float(
                            post.get('sun_from_' + str(i)).replace(":", ".")),
                        'sun_to': float(
                            post.get('sun_to_' + str(i)).replace(":", ".")),
                        'group_id': group.id,
                        'is_recurrent': post.get('sun_recurrent_' + str(i)),
                        'venue_id': int(
                            post.get('sun_venue_' + str(i))) if post.get(
                            'sun_venue_' + str(i)) else False,
                    })
        group.sudo().write(values)
        return request.redirect('/group/%s' % group.id)

    @http.route('/get_venues', auth='user', type='json', website=True)
    def get_venues(self, **kwargs):
        org_domain = []
        if request.env.user.has_group(
                'organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        elif request.env.user.has_group(
                'organisation.group_organisation_coaches'):
            coach_ids = request.env['organisation.coaches'].search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            organisations = coach_ids.mapped('organisation_ids')
            org_domain.append(('id', 'in', organisations.ids))
        elif request.env.user.has_group(
                'organisation.group_organisation_athletes'):
            athlete_ids = request.env['organisation.athletes'].search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            organisations = athlete_ids.mapped('organisation_ids')
            org_domain.append(('id', 'in', organisations.ids))
        elif request.env.user.has_group(
                'organisation.group_organisation_parents'):
            parents = request.env['organisation.parents'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            organisations = parents.mapped('organisation_ids')
            org_domain.append(('id', 'in', organisations.ids))
        else:
            raise AccessError(
                _("Sorry you are not allowed to access this document"))
        # if request.env.user.has_group(
        #         'organisation.group_organisation_athletes'):
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        print(org_domain)

        venues = request.env['organisation.venues'].sudo().search(
            [])
        organisation = None
        if org_domain:
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1)
            print(organisation)
            if organisation:
                venues = venues.search(
                    [('organisation_ids', 'in', [organisation.id])])
        venue_ids = []
        for venue in venues:
            venue_ids.append([venue.display_name, venue.id])
        return {
            'venues': venue_ids,
        }

    @http.route('/delete/mon/schedule',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_schedule(self, **post):
        if post.get('id'):
            mon_schedule = request.env['group.mon.schedule'].sudo().browse(int(post.get('id')))
            group = mon_schedule.group_id.id
            mon_schedule.unlink()
            return request.redirect('/group/%s' % group)

    @http.route('/delete/tue/schedule',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_tue_schedule(self, **post):
        if post.get('id'):
            tue_schedule = request.env['group.tue.schedule'].sudo().browse(
                int(post.get('id')))
            group = tue_schedule.group_id.id
            tue_schedule.unlink()
            return request.redirect('/group/%s' % group)

    @http.route('/delete/wed/schedule',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_wed_schedule(self, **post):
        if post.get('id'):
            wed_schedule = request.env['group.wed.schedule'].sudo().browse(
                int(post.get('id')))
            group = wed_schedule.group_id.id
            wed_schedule.unlink()
            return request.redirect('/group/%s' % group)

    @http.route('/delete/thu/schedule',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_thu_schedule(self, **post):
        if post.get('id'):
            thu_schedule = request.env['group.thu.schedule'].sudo().browse(
                int(post.get('id')))
            group = thu_schedule.group_id.id
            thu_schedule.unlink()
            return request.redirect('/group/%s' % group)

    @http.route('/delete/fri/schedule',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_fri_schedule(self, **post):
        if post.get('id'):
            fri_schedule = request.env['group.fri.schedule'].sudo().browse(
                int(post.get('id')))
            group = fri_schedule.group_id.id
            fri_schedule.unlink()
            return request.redirect('/group/%s' % group)

    @http.route('/delete/sat/schedule',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_sat_schedule(self, **post):
        if post.get('id'):
            sat_schedule = request.env['group.sat.schedule'].sudo().browse(
                int(post.get('id')))
            group = sat_schedule.group_id.id
            sat_schedule.unlink()
            return request.redirect('/group/%s' % group)

    @http.route('/delete/sun/schedule',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_sun_schedule(self, **post):
        if post.get('id'):
            sun_schedule = request.env['group.sun.schedule'].sudo().browse(
                int(post.get('id')))
            group = sun_schedule.group_id.id
            sun_schedule.unlink()
            return request.redirect('/group/%s' % group)

    @http.route('/my/registers',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def my_registers(self, page=1, search=''):
        domain = []
        if search:
            domain.append(('name', 'ilike', search))
        org_domain = []
        if request.env.user.has_group(
                'organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        elif request.env.user.has_group(
                'organisation.group_organisation_coaches'):
            coach_ids = request.env['organisation.coaches'].search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            organisations = coach_ids.mapped('organisation_ids')
            org_domain.append(('id', 'in', organisations.ids))
        elif request.env.user.has_group(
                'organisation.group_organisation_athletes'):
            athlete_ids = request.env['organisation.athletes'].search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            organisations = athlete_ids.mapped('organisation_ids')
            org_domain.append(('id', 'in', organisations.ids))
        elif request.env.user.has_group(
                'organisation.group_organisation_parents'):
            parents = request.env['organisation.parents'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            organisations = parents.mapped('organisation_ids')
            org_domain.append(('id', 'in', organisations.ids))
        else:
            raise AccessError(
                _("Sorry you are not allowed to access this document"))
        registers = request.env['organisation.registers'].sudo().search(
            domain)
        print(domain)
        total = len(registers)
        pager = request.website.pager(
            url='/my/registers',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        registers = registers[offset: offset + 6]
        # if request.env.user.has_group(
        #         'organisation.group_organisation_athletes'):
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        print(org_domain)

        venues = request.env['organisation.venues'].sudo().search(
            [])
        coaches = request.env['organisation.coaches'].sudo().search([])
        athletes = request.env['organisation.athletes'].sudo().search([])
        groups = request.env['athlete.groups'].sudo().search([])
        organisation = None
        if org_domain:
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1)
            print(organisation)
            if organisation:
                venues = venues.search(
                    [('organisation_ids', 'in', [organisation.id])])
                coaches = coaches.search(
                    [('organisation_ids', 'in', [organisation.id])])
                athletes = athletes.search([('organisation_ids', 'in', [organisation.id])])
                groups = groups.search([('organisation_ids', 'in', [organisation.id])])
        values = {
            'search': search,
            'registers': registers,
            'total': total,
            'pager': pager,
            'is_account': True,
            'venues': venues,
            'athletes': athletes,
            'coaches': coaches,
            'groups': groups,
            }
        return request.render('organisation_registers.registers_template', values)

    @http.route(['/my/register/<int:register_id>'], type='http',
                auth='user', csrf=False, website=True,
                method='POST'
                )
    def register_details(self, **kwargs):
        print(kwargs.get('register_id'), "register_id")
        register = request.env['organisation.registers'].browse(
            int(kwargs.get('register_id')))
        return request.render('organisation_registers.registers_details_template',
                              {'register': register, 'is_account': True})

    @http.route(['/update/register'], type='http',
                auth='user', csrf=False, website=True,
                method='POST'
                )
    def update_register(self, **post):
        print(post)
        register = request.env['organisation.registers'].browse(
            int(post.get('register')))
        print(register, "register")
        keys = post.keys()
        key_list = []
        for key in keys:
            if len(key.split('_')) > 1:
                key_list.append(key.split('_')[2])
        print(key_list, "key_list")
        maximum = 1
        minimum = 1
        if key_list:
            str_list = [x for x in key_list if x != '']
            maximum = max(list(set(str_list)))
            minimum = min(list(set(str_list)))
            print(maximum, "maximum")
            print(minimum, "minimum")
        for i in range(int(minimum), int(maximum) + 1):
            if post.get('attendee_name_' + str(i)):
                attendee_id = request.env['organisation.registers.attendees'].sudo().browse(int(post.get('attendee_id_' + str(i))))
                attendee_id.sudo().write({
                    'is_attended': True if post.get('is_attendee_' + str(i)) == 'on' else False,
                })
                print(post.get('is_attendee_' + str(i)), "minimum")
        return request.redirect('/my/register/%s' % register.id)

    @http.route('/get_groups', auth='user', type='json', website=True)
    def get_groups(self, **kwargs):
        print(kwargs, "kwargs")
        coaches = request.env['organisation.coaches'].sudo().browse(int(kwargs.get('coach')))
        groups = request.env['athlete.groups'].sudo().search([('coach_ids', 'in', [coaches.id])])
        group_ids = []
        for rec in groups:
            group_ids.append([rec.name, rec.id])
        return {'groups': group_ids}

    @http.route('/get_athletes', auth='user', type='json', website=True)
    def get_athletes(self, **kwargs):
        print(kwargs, "kwargs")
        group = request.env['athlete.groups'].sudo().browse(
            int(kwargs.get('group')))
        print(group, "group")
        athlete_ids = []
        for athlete in group.athlete_ids:
            athlete_ids.append([athlete.name, athlete.id])
        print(athlete_ids, "athlete_ids")
        # groups = request.env['athlete.groups'].sudo().search(
        #     [('coach_ids', 'in', [coaches.id])])
        # group_ids = []
        # for rec in groups:
        #     group_ids.append([rec.name, rec.id])
        return {'athletes': athlete_ids}

    @http.route('/create/registers', auth='user', type='http', website=True)
    def create_registers(self, **post):
        print(post, "post")
        athlete_ids = list(
            map(int, request.httprequest.form.getlist('athletes')))
        events = request.env['calendar.event'].sudo().search([('start', '>=', post.get('date') + ' 00:00:00'), ('start', '<=', post.get('date') + ' 23:59:59')])
        print(events, "events")
        for event in events.filtered(lambda x: not x.register_id):
            values = {
                'name': event.name,
                'coach_id': int(post.get('coach')) if post.get('coach') else False,
                'date': post.get('date'),
                'group_id': int(post.get('group')) if post.get('group') else False,
                'attendee_ids': [
                    (0, 0, {'attendee_id': attendee}) for attendee in athlete_ids
                ],
                'event_id': event.id,
            }
            register_id = request.env['organisation.registers'].sudo().create(values)
            event.register_id = register_id.id
        return request.redirect('/my/registers')
