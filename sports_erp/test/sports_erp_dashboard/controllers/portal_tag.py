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

    @http.route('/discipline_tag', auth='user', type='json',
                website=True)
    def ajax_discipline_tag(self, **post):
        discipline_tag = request.env['discipline.tags'].create({
            'name': post.get('tag_name'),
        })
        return {
            'name': discipline_tag.name,
            'id': discipline_tag.id
        }

    @http.route('/fan_tag', auth='user', type='json',
                website=True)
    def ajax_fan_tag(self, **post):
        fan_tag = request.env['fans.tags'].create({
            'name': post.get('tag_name'),
        })
        return {
            'name': fan_tag.name,
            'id': fan_tag.id
        }

    @http.route('/athlete_tag', auth='user', type='json',
                website=True)
    def ajax_athlete_tag(self, **post):
        athlete_tag = request.env['athletes.tags'].create({
            'name': post.get('tag_name'),
        })
        print(athlete_tag)
        return {
            'name': athlete_tag.name,
            'id': athlete_tag.id
        }

    @http.route('/coach_tag', auth='user', type='json',
                website=True)
    def ajax_coach_tag(self, **post):
        coach_tag = request.env['coaches.tags'].create({
            'name': post.get('tag_name'),
        })
        print(coach_tag)
        return {
            'name': coach_tag.name,
            'id': coach_tag.id
        }

    @http.route('/venues_tag', auth='user', type='json',
                website=True)
    def ajax_venues_tag(self, **post):
        venues_tag = request.env['venues.tags'].create({
            'name': post.get('tag_name'),
        })
        print(venues_tag)
        return {
            'name': venues_tag.name,
            'id': venues_tag.id
        }

    @http.route('/parents_tag', auth='user', type='json',
                website=True)
    def ajax_parents_tag(self, **post):
        parents_tag = request.env['parents.tags'].create({
            'name': post.get('tag_name'),
        })
        print(parents_tag)
        return {
            'name': parents_tag.name,
            'id': parents_tag.id
        }

    @http.route('/group_tag', auth='user', type='json',
                website=True)
    def ajax_group_tag(self, **post):
        group_tag = request.env['group.tags'].create({
            'name': post.get('tag_name'),
        })
        print(group_tag)
        return {
            'name': group_tag.name,
            'id': group_tag.id
        }

    @http.route('/discipline_tag', auth='user', type='json',
                website=True)
    def ajax_discipline_tag(self, **post):
        discipline_tag = request.env['discipline.tags'].create({
            'name': post.get('tag_name'),
        })
        print(discipline_tag)
        return {
            'name': discipline_tag.name,
            'id': discipline_tag.id
        }
