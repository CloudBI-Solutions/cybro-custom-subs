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


class AssessmentValue(CustomerPortal):

    @http.route('/assessment_field_value', auth='user', type='json',
                website=True)
    def assessment_field_value(self, **post):
        print('Assessment', post)
        assessment_list = [int(i) for i in post.get('assessment_ids')]
        assessment_val = request.env['assessment.types'].sudo().browse(
            assessment_list)
        print('Assessment', assessment_val)
        return_assessment = []
        for rec in assessment_val:
            return_assessment.append({'id': rec.id, 'name': rec.name})
        print('Assessment', return_assessment)
        return return_assessment
