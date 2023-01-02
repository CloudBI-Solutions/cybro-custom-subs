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


class Organisation(CustomerPortal):
    @http.route('/my/profile', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def my_profile(self, **post):
        if request.env.user.has_group('organisation.group_organisation_administrator'):
            org_domain = [('allowed_user_ids', 'in', [request.env.user.id])]
            if request.httprequest.cookies.get('select_organisation') is not None:
                org_domain.append(('id', '=',
                                   request.httprequest.cookies.get(
                                       'select_organisation')))
            organisation = request.env[
                'organisation.organisation'].sudo().search(org_domain,
                                                           limit=1)
        elif request.env.user.has_group('organisation.group_organisation_athletes'):
                organisation = request.env['organisation.athletes'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)])
        elif request.env.user.has_group(
                'organisation.group_organisation_coaches'):
            organisation = request.env['organisation.coaches'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])
        elif request.env.user.has_group(
                'organisation.group_organisation_parents'):
            organisation = request.env['organisation.parents'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])

        return request.render('sports_erp_dashboard.my_profile_template',
                              {'organisation': organisation if organisation else None,
                               'is_account': True})
    
    @route(['/my/update_profile'],
           type='http', auth="user", website=True,
           method='POST')
    def update_profile(self, **post):
        if request.env.user.has_group('organisation.group_organisation_administrator'):
            organisation = request.env['organisation.organisation'].browse(
                int(post.get('organisation_id'))
            )
        elif request.env.user.has_group('organisation.group_organisation_athletes'):
                organisation = request.env['organisation.athletes'].browse(
                int(post.get('organisation_id'))
            )
        elif request.env.user.has_group(
                'organisation.group_organisation_coaches'):
            organisation = request.env['organisation.coaches'].browse(
                int(post.get('organisation_id'))
            )
        elif request.env.user.has_group(
                'organisation.group_organisation_parents'):
            organisation = request.env['organisation.parents'].browse(
                int(post.get('organisation_id'))
            )

        values = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
        }
        organisation.partner_id.sudo().write({
            'image_1920': base64.b64encode(
                post.get('photo').read()) if post.get('photo') else organisation.partner_id.image_1920,
            'last_name': post.get('last_name')
        })
        organisation.sudo().write(values)
        return request.redirect('/my/profile')
