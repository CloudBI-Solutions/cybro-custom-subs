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
    @route(['/my/update_profile'],
           type='http', auth="user", website=True,
           method='POST')
    def update_profile(self, **post):
        organisation = request.env['organisation.organisation'].browse(
            int(post.get('organisation_id'))
        )
        values = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'img_organisation': base64.b64encode(
                post.get('photo').read()) if post.get('photo') else False
        }
        organisation.partner_id.sudo().write({
            'image_1920': values['img_organisation']
        })
        organisation.sudo().write(values)
        return request.redirect('/my/profile')
