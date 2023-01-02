import base64
import json

from odoo.addons.http_routing.models.ir_http import slug
from odoo import fields, _
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager
from collections import OrderedDict
from odoo.http import request, route
from odoo.addons.base.models.res_partner import _tz_get
from datetime import datetime, date
from odoo.addons.website_sale.controllers.main import WebsiteSale
from dateutil.relativedelta import relativedelta
import pytz


class HomePortal(CustomerPortal):
    @route(['/my/edit_home_image'], type='http', auth="user", website=True)
    def edit_home_image(self):
        domain = []
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        print(organisation)
        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))

        domain.append(('company_id', '=', request.env.user.company_id.id))
        home_images = request.env['home.image'].sudo().search(
            domain)
        print(home_images, "home_images")
        values = {
            'home_images': home_images,
            'is_account': True,
            'organisation': organisation,
        }
        print('home_images', home_images)
        return request.render(
            'sports_erp_dashboard.sports_erp_portal_home_edit', values)

    @route(['/my/edit_gallery_image'], type='http', auth="user", website=True)
    def edit_gallery_image(self):
        domain = []
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        print(organisation)
        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))

        domain.append(('company_id', '=', request.env.user.company_id.id))
        home_images = request.env['home.gallery'].sudo().search(
            domain)
        values = {
            'is_account': True,
            'home_images': home_images
        }
        return request.render(
            'sports_erp_dashboard.sports_erp_portal_gallery_edit', values)

