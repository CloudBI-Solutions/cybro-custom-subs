import base64

import json
from odoo import fields, _
import logging
from odoo import http
from odoo.http import request, route
from datetime import datetime
import pytz
from datetime import timedelta
from odoo.addons.website.controllers import form

from odoo.exceptions import AccessError, MissingError, UserError


class BadmintooVideoController(http.Controller):
    @route(['/upload/sr_videos'], type='http',
           auth='user', website=True, methods=['POST', 'GET'])
    def upload_sr_videos(self, **post):
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment_id')))
        print(assessment)
        attachments = request.env['ir.attachment']
        if post.get('service_video'):
            attachment_service = attachments.sudo().create({
                'name': post.get('service_video').filename,
                'type': 'binary',
                'datas': base64.b64encode(
                    post.get('service_video').read()),
                'res_model': assessment._name,
                'res_id': assessment.id,
            })
            assessment.sudo().write({
                'attachment_ids': [(4, attachment_service.id)],
                'service_video': attachment_service.datas,
                'receiving_video': attachment_service.datas,
            })

