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


class BadmintoProducts(CustomerPortal):
    @http.route(['/badmintoo_products', '/badmintoo_products/page/<int:page>', '/badmintoo_products', '/badmintoo_products/page/<int:page>'],
                type='http', auth="user", website=True)
    def badmintoproducts(self, page=1, search=''):
        badminto_products = request.env['product.product'].sudo().search([])
        org_domain = []
        if request.env.user.has_group('organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        else:
            org_domain.append(('id', 'in', request.env.user.partner_id.organisation_ids.ids))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        domain = [('is_badminto_product', '=', True),
                  ('is_published', '=', True),
                  ('organisation_ids', '=', organisation.id)
                  ]

        if search:
            domain.append(('name', 'ilike', search))
        badminto_products = badminto_products.sudo().search(domain)
        return request.render('badminto.badminto_home_template',
                              {'badminto_products': badminto_products,
                               'is_account': True
                              })
