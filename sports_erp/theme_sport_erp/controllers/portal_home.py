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


class Pricing(CustomerPortal):

    @route('/pricing', type='http', auth="public", website=True)
    def pricing(self, **post):
        subscription_products = request.env['product.product'].sudo().search(
            [('organisation_stage_id', '!=', False)], limit=3,
            order='lst_price ASC')
        return request.render("theme_sport_erp.pricing_template",
                              {'is_home': True,
                               'products': subscription_products})

    @route('/core_modules', type='http', auth="public", website=True)
    def core_modules(self, **post):
        return request.render("theme_sport_erp.core_modules",
                              {'is_home': True})

    @route('/sport_business_management',
           type='http', auth="public", website=True)
    def sport_business_management(self, **post):
        return request.render("theme_sport_erp.sport_business_management",
                              {'is_home': True})

    @route('/company_and_backend_access',
           type='http', auth="public", website=True)
    def company_and_backend_access(self, **post):
        return request.render("theme_sport_erp.company_and_backend_access",
                              {'is_home': True})

    @route('/performance_and_customizations',
           type='http', auth="public", website=True)
    def performance_and_customizations(self, **post):
        return request.render("theme_sport_erp.performance_and_customization",
                              {'is_home': True})

    @route('/features', type='http', auth="public", website=True)
    def choose_modules(self, **post):
        return request.render("theme_sport_erp.choose_modules",
                              {'is_home': True})

    @http.route('/sport_erp_cart', auth='public', type='json', website=True)
    def sport_erp_cart(self, **post):
        print('**post', post)
        order = request.website.sale_get_order(force_create=1)
        orderline = order.order_line.filtered(
            lambda x: x.product_id.id == int(post.get('product_id')))
        if not orderline:
            order_line = request.env['sale.order.line'].sudo().create({
                'product_id': int(post.get('product_id')),
                'product_uom_qty': 1,
                'order_id': order.id,
            })
        else:
            for rec in orderline:
                rec.write({
                    'product_uom_qty': orderline.product_uom_qty + 1
                })
        return '/shop/cart'
