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
        print(post)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment_id')))
        if post.get('service_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'service_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('service_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'service_video',
                'name': post.get('service_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('service_video').read())
            })
        if post.get('receiving_video'):
            print(post.get('receiving_video'))
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'receiving_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('receiving_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'receiving_video',
                'name': post.get('receiving_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('receiving_video').read())
            })
        return request.redirect('/my/assessment?assessment=%s' % assessment.id)

    @route(['/upload/fnz_videos/'], type='http',
           auth='user', website=True, methods=['POST', 'GET'])
    def upload_fnz_videos(self, **post):
        print('fnz_video', post)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment_id')))
        if post.get('fnz_to_fnk_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_to_fnk_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(
                post.get('fnz_to_fnk_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_to_fnk_video',
                'name': post.get('fnz_to_fnk_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_to_fnk_video').read())
            })
        if post.get('fnz_co_fnp_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_co_fnp_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_co_fnp_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_co_fnp_video',
                'name': post.get('fnz_co_fnp_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_co_fnp_video').read())
            })

        if post.get('fnz_co_ofcn_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_co_ofcn_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_co_ofcn_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_co_ofcn_video',
                'name': post.get('fnz_co_ofcn_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_co_ofcn_video').read())
            })

        if post.get('fnz_co_fol_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_co_fol_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_co_fol_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_co_fol_video',
                'name': post.get('fnz_co_fol_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_co_fol_video').read())
            })

        if post.get('fnz_co_fss_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_co_fss_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_co_fss_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_co_fss_video',
                'name': post.get('fnz_co_fss_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_co_fss_video').read())
            })

        if post.get('fnz_co_frs_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_co_frs_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_co_frs_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_co_frs_video',
                'name': post.get('fnz_co_frs_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_co_frs_video').read())
            })

        if post.get('fnz_co_nb_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_co_nb_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_co_nb_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_co_nb_video',
                'name': post.get('fnz_co_nb_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_co_nb_video').read())
            })

        if post.get('fnz_frs_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_frs_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_frs_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_frs_video',
                'name': post.get('fnz_frs_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_frs_video').read())
            })

        if post.get('fnz_neutralisation_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_neutralisation_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_neutralisation_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_neutralisation_video',
                'name': post.get('fnz_neutralisation_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_neutralisation_video').read())
            })

        if post.get('fnz_cd_dfcn_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_cd_dfcn_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_cd_dfcn_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_cd_dfcn_video',
                'name': post.get('fnz_cd_dfcn_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_cd_dfcn_video').read())
            })

        if post.get('fnz_cd_dfl_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_cd_dfl_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_cd_dfl_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_cd_dfl_video',
                'name': post.get('fnz_cd_dfl_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_cd_dfl_video').read())
            })

        if post.get('fnz_td_dd_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fnz_td_dd_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fnz_td_dd_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fnz_td_dd_video',
                'name': post.get('fnz_td_dd_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fnz_td_dd_video').read())
            })
        return request.redirect('/my/assessment?assessment=%s' % assessment.id)

    @route(['/upload/bnz_videos/'], type='http',
           auth='user', website=True, methods=['POST', 'GET'])
    def upload_bnz_videos(self, **post):
        print('bnz_video', post)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment_id')))
        if post.get('bnz_to_fnk_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_to_fnk_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(
                post.get('bnz_to_fnk_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_to_fnk_video',
                'name': post.get('bnz_to_fnk_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_to_fnk_video').read())
            })
        if post.get('bnz_co_fnp_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_co_fnp_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_co_fnp_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_co_fnp_video',
                'name': post.get('bnz_co_fnp_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_co_fnp_video').read())
            })

        if post.get('bnz_co_ofcn_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_co_ofcn_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_co_ofcn_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_co_ofcn_video',
                'name': post.get('bnz_co_ofcn_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_co_ofcn_video').read())
            })

        if post.get('bnz_co_fol_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_co_fol_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_co_fol_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_co_fol_video',
                'name': post.get('bnz_co_fol_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_co_fol_video').read())
            })

        if post.get('bnz_co_fss_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_co_fss_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_co_fss_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_co_fss_video',
                'name': post.get('bnz_co_fss_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_co_fss_video').read())
            })

        if post.get('bnz_co_frs_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_co_frs_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_co_frs_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_co_frs_video',
                'name': post.get('bnz_co_frs_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_co_frs_video').read())
            })

        if post.get('bnz_co_nb_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_co_nb_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_co_nb_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_co_nb_video',
                'name': post.get('bnz_co_nb_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_co_nb_video').read())
            })

        if post.get('bnz_frs_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_frs_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_frs_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_frs_video',
                'name': post.get('bnz_frs_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_frs_video').read())
            })

        if post.get('bnz_neutralisation_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_neutralisation_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_neutralisation_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_neutralisation_video',
                'name': post.get('bnz_neutralisation_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_neutralisation_video').read())
            })

        if post.get('bnz_cd_dfcn_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_cd_dfcn_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_cd_dfcn_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_cd_dfcn_video',
                'name': post.get('bnz_cd_dfcn_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_cd_dfcn_video').read())
            })

        if post.get('bnz_cd_dfl_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_cd_dfl_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_cd_dfl_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_cd_dfl_video',
                'name': post.get('bnz_cd_dfl_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_cd_dfl_video').read())
            })

        if post.get('bnz_td_dd_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bnz_td_dd_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('bnz_td_dd_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bnz_td_dd_video',
                'name': post.get('bnz_td_dd_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bnz_td_dd_video').read())
            })
        return request.redirect('/my/assessment?assessment=%s' % assessment.id)

    @route(['/upload/fmz_videos/'], type='http',
           auth='user', website=True, methods=['POST', 'GET'])
    def upload_fmz_videos(self, **post):
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment_id')))
        if post.get('fmz_co_ss_video'):
            print('fmzzzzz present')
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fmz_co_ss_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(
                post.get('fmz_co_ss_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fmz_co_ss_video',
                'name': post.get('fmz_co_ss_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fmz_co_ss_video').read())
            })
        if post.get('fmz_fmcp_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fmz_fmcp_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fmz_fmcp_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fmz_fmcp_video',
                'name': post.get('fmz_fmcp_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fmz_fmcp_video').read())
            })

        if post.get('fmz_cd_fds_s_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fmz_cd_fds_s_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fmz_cd_fds_s_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fmz_cd_fds_s_video',
                'name': post.get('fmz_cd_fds_s_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fmz_cd_fds_s_video').read())
            })

        if post.get('fmz_cd_fdc_s_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fmz_cd_fdc_s_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fmz_cd_fdc_s_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fmz_cd_fdc_s_video',
                'name': post.get('fmz_cd_fdc_s_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fmz_cd_fdc_s_video').read())
            })

        if post.get('fmz_cd_fds_l_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fmz_cd_fds_l_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fmz_cd_fds_l_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fmz_cd_fds_l_video',
                'name': post.get('fmz_cd_fds_l_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fmz_cd_fds_l_video').read())
            })

        if post.get('fmz_cd_fdc_l_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fmz_cd_fdc_l_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fmz_cd_fdc_l_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fmz_cd_fdc_l_video',
                'name': post.get('fmz_cd_fdc_l_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fmz_cd_fdc_l_video').read())
            })

        if post.get('fmz_cd_fdca_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fmz_cd_fdca_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fmz_cd_fdca_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fmz_cd_fdca_video',
                'name': post.get('fmz_cd_fdca_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fmz_cd_fdca_video').read())
            })

        if post.get('fmz_fd_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'fmz_fd_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(post.get('fmz_fd_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'fmz_fd_video',
                'name': post.get('fmz_fd_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('fmz_fd_video').read())
            })
        return request.redirect('/my/assessment?assessment=%s' % assessment.id)

    @route(['/upload/bmz_videos/'], type='http',
           auth='user', website=True, methods=['POST', 'GET'])
    def upload_bmz_videos(self, **post):
        print('bmz_video', post)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment_id')))
        if post.get('bmz_co_ss_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bmz_co_ss_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(
                post.get('bmz_co_ss_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bmz_co_ss_video',
                'name': post.get('bmz_co_ss_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bmz_co_ss_video').read())
            })
        if post.get('bmz_bmcp_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bmz_bmcp_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('bmz_bmcp_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bmz_bmcp_video',
                'name': post.get('bmz_bmcp_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bmz_bmcp_video').read())
            })
        if post.get('bmz_cd_bds_s_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bmz_cd_bds_s_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('bmz_cd_bds_s_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bmz_cd_bds_s_video',
                'name': post.get('bmz_cd_bds_s_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bmz_cd_bds_s_video').read())
            })
        if post.get('bmz_cd_bdc_s_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bmz_cd_bdc_s_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('bmz_cd_bdc_s_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bmz_cd_bdc_s_video',
                'name': post.get('bmz_cd_bdc_s_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bmz_cd_bdc_s_video').read())
            })
        if post.get('bmz_cd_bds_l_video'):
            print('herree')
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bmz_cd_bds_l_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('bmz_cd_bds_l_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bmz_cd_bds_l_video',
                'name': post.get('bmz_cd_bds_l_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bmz_cd_bds_l_video').read())
            })
        if post.get('bmz_cd_bdc_l_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bmz_cd_bdc_l_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('bmz_cd_bdc_l_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bmz_cd_bdc_l_video',
                'name': post.get('bmz_cd_bdc_l_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bmz_cd_bdc_l_video').read())
            })
        if post.get('bmz_cd_bdc_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bmz_cd_bdc_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('bmz_cd_bdc_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bmz_cd_bdc_video',
                'name': post.get('bmz_cd_bdc_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bmz_cd_bdc_video').read())
            })
        if post.get('bmz_td_bd_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'bmz_td_bd_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('bmz_td_bd_video').read())).split("b'")[
                1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'bmz_td_bd_video',
                'name': post.get('bmz_td_bd_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('bmz_td_bd_video').read())
            })
        return request.redirect('/my/assessment?assessment=%s' % assessment.id)

    @route(['/upload/rcovhz_videos/'], type='http',
           auth='user', website=True, methods=['POST', 'GET'])
    def upload_rcovhz_videos(self, **post):
        print('rcovhz_video', post)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment_id')))
        if post.get('rcovhz_to_js_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcovhz_to_js_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(
                post.get('rcovhz_to_js_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcovhz_to_js_video',
                'name': post.get('rcovhz_to_js_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcovhz_to_js_video').read())
            })

        if post.get('rcovhz_to_frs_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcovhz_to_frs_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('rcovhz_to_frs_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcovhz_to_frs_video',
                'name': post.get('rcovhz_to_frs_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcovhz_to_frs_video').read())
            })

        if post.get('rcovhz_to_co_ss_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcovhz_to_co_ss_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('rcovhz_to_co_ss_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcovhz_to_co_ss_video',
                'name': post.get('rcovhz_to_co_ss_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcovhz_to_co_ss_video').read())
            })

        if post.get('rcovhz_co_oc_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcovhz_co_oc_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('rcovhz_co_oc_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcovhz_co_oc_video',
                'name': post.get('rcovhz_co_oc_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcovhz_co_oc_video').read())
            })

        if post.get('rcovhz_co_orc_video'):
            print('herree')
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcovhz_co_orc_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('rcovhz_co_orc_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcovhz_co_orc_video',
                'name': post.get('rcovhz_co_orc_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcovhz_co_orc_video').read())
            })

        if post.get('rcovhz_co_ooc_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcovhz_co_ooc_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('rcovhz_co_ooc_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcovhz_co_ooc_video',
                'name': post.get('rcovhz_co_ooc_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcovhz_co_ooc_video').read())
            })

        if post.get('rcovhz_oc_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcovhz_oc_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
            str(base64.b64encode(post.get('rcovhz_oc_video').read())).split(
                "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcovhz_oc_video',
                'name': post.get('rcovhz_oc_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcovhz_oc_video').read())
            })
        return request.redirect('/my/assessment?assessment=%s' % assessment.id)

    @route(['/upload/rcbz_videos/'], type='http',
           auth='user', website=True, methods=['POST', 'GET'])
    def upload_rcbz_videos(self, **post):
        print('rcbz_video', post)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment_id')))
        if post.get('rcbz_co_obc_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcbz_co_obc_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(
                post.get('rcbz_co_obc_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcbz_co_obc_video',
                'name': post.get('rcbz_co_obc_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcbz_co_obc_video').read())
            })

        if post.get('rcbz_co_brd_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcbz_co_brd_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcbz_co_brd_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcbz_co_brd_video',
                'name': post.get('rcbz_co_brd_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcbz_co_brd_video').read())
            })

        if post.get('rcbz_bcd_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcbz_bcd_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcbz_bcd_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcbz_bcd_video',
                'name': post.get('rcbz_bcd_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcbz_bcd_video').read())
            })

        if post.get('rcbz_cd_ns_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcbz_cd_ns_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcbz_cd_ns_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcbz_cd_ns_video',
                'name': post.get('rcbz_cd_ns_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcbz_cd_ns_video').read())
            })

        if post.get('rcbz_cd_nc_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcbz_cd_nc_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcbz_cd_nc_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcbz_cd_nc_video',
                'name': post.get('rcbz_cd_nc_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcbz_cd_nc_video').read())
            })

        return request.redirect('/my/assessment?assessment=%s' % assessment.id)

    @route(['/upload/rcfz_videos/'], type='http',
           auth='user', website=True, methods=['POST', 'GET'])
    def upload_rcfz_videos(self, **post):
        print('rcfz_video', post)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment_id')))
        if post.get('rcfz_to_js_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcfz_to_js_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(
                post.get('rcfz_to_js_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcfz_to_js_video',
                'name': post.get('rcfz_to_js_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcfz_to_js_video').read())
            })

        if post.get('rcfz_to_fbrs_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcfz_to_fbrs_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcfz_to_fbrs_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcfz_to_fbrs_video',
                'name': post.get('rcfz_to_fbrs_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcfz_to_fbrs_video').read())
            })

        if post.get('rcfz_co_oc_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcfz_co_oc_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcfz_co_oc_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcfz_co_oc_video',
                'name': post.get('rcfz_co_oc_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcfz_co_oc_video').read())
            })

        if post.get('rcfz_co_fcs_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcfz_co_fcs_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcfz_co_fcs_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcfz_co_fcs_video',
                'name': post.get('rcfz_co_fcs_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('rcfz_co_fcs_video').read())
            })

        if post.get('rcfz_co_fcc_video'):
            print('herree')
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcfz_co_fcc_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcfz_co_fcc_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcfz_co_fcc_video',
                'name': post.get('rcfz_co_fcc_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcfz_co_fcc_video').read())
            })

        if post.get('rcfz_co_fnd_video'):
            print('herree')
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcfz_co_fnd_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcfz_co_fnd_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcfz_co_fnd_video',
                'name': post.get('rcfz_co_fnd_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcfz_co_fnd_video').read())
            })

        if post.get('rcfz_co_frcs_video'):
            print('herree')
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcfz_co_frcs_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcfz_co_frcs_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcfz_co_frcs_video',
                'name': post.get('rcfz_co_frcs_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcfz_co_frcs_video').read())
            })

        if post.get('rcfz_co_dc_video'):
            print('herree')
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcfz_co_dc_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcfz_co_dc_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcfz_co_dc_video',
                'name': post.get('rcfz_co_dc_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcfz_co_dc_video').read())
            })

        if post.get('rcfz_fn_video'):
            print('herree')
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcfz_fn_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcfz_fn_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcfz_fn_video',
                'name': post.get('rcfz_fn_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcfz_fn_video').read())
            })

        if post.get('rcfz_td_fd_video'):
            print('herree')
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'rcfz_td_fd_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('rcfz_td_fd_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'rcfz_td_fd_video',
                'name': post.get('rcfz_td_fd_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('rcfz_td_fd_video').read())
            })
        return request.redirect('/my/assessment?assessment=%s' % assessment.id)

    @route(['/upload/footwork_videos/'], type='http',
           auth='user', website=True, methods=['POST', 'GET'])
    def upload_footwork_videos(self, **post):
        print('footwork_video', post)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment_id')))
        if post.get('footwork_ofp_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'footwork_ofp_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = str(base64.b64encode(
                post.get('footwork_ofp_video').read())).split("b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'footwork_ofp_video',
                'name': post.get('footwork_ofp_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(post.get('footwork_ofp_video').read())
            })

        if post.get('footwork_dfp_video'):
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', assessment.id),
                ('badminto_field_name', '=', 'footwork_dfp_video')
            ])
            if attachment:
                attachment.unlink()
            baseto64 = \
                str(base64.b64encode(
                    post.get('footwork_dfp_video').read())).split(
                    "b'")[1]
            file_data = 'data:video/mp4;base64,' + baseto64
            request.env['ir.attachment'].sudo().create({
                'res_model': 'badminto.assessment',
                'res_id': assessment.id,
                'type': 'binary',
                'badminto_field_name': 'footwork_dfp_video',
                'name': post.get('footwork_dfp_video').filename,
                'badminto_video_file_data': file_data,
                'datas': base64.b64encode(
                    post.get('footwork_dfp_video').read())
            })
        return request.redirect('/my/assessment?assessment=%s' % assessment.id)
