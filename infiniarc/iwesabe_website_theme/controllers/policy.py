from odoo import http, models, tools, fields, _
from odoo.http import Controller, request, route, content_disposition
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.auth_signup.models.res_users import SignupError
import logging
import werkzeug
from odoo.exceptions import UserError


class WebsitePolicyController(http.Controller):

    @http.route(['/return_policy'], type='http', auth="public", website=True)
    def website_retun_policy(self, **post):
        value = {}

        return request.render("iwesabe_website_theme.website_return_policy", value)

    @http.route(['/shipping_policy'], type='http', auth="public", website=True)
    def website_shipping_policy(self, **post):
        value = {}

        return request.render("iwesabe_website_theme.website_shipping_policy", value)
