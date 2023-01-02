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


class FanTag(CustomerPortal):

    @http.route(['/create/fan_tag'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def create_fan_tags(self, **post):
        print("post", post)
        request.env['fans.tags'].create({
            'name': post.get('tag_name'),
        })

    @http.route(['/create/athlete_tag'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def create_athlete_tags(self, **post):
        print("post", post)
        request.env['athletes.tags'].create({
            'name': post.get('tag_name'),
        })

    @http.route(['/create/coach_tag'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def create_coach_tags(self, **post):
        print("post", post)
        request.env['coaches.tags'].create({
            'name': post.get('tag_name'),
        })

    @http.route(['/create/group_tag'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def my_group_tag(self, **post):
        print("post", post)
        request.env['group.tags'].create({
            'name': post.get('tag_name'),
        })

    @http.route(['/create/parent_tag'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def my_parents_tag(self, **post):
        print("post", post)
        request.env['parents.tags'].create({
            'name': post.get('tag_name'),
        })

    @http.route(['/create/discipline_tag'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def my_discipline_tag(self, **post):
        print("post", post)
        request.env['discipline.tags'].create({
            'name': post.get('tag_name'),
        })

    @http.route(['/create/venue_tag'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def my_venue_tag(self, **post):
        print("post", post)
        request.env['venues.tags'].create({
            'name': post.get('tag_name'),
        })


