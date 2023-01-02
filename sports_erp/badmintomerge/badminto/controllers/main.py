
import json
from odoo import fields, _
import logging
from odoo import http
from odoo.http import request, route
from odoo.addons.survey.controllers.main import Survey
import werkzeug
from datetime import datetime
import pytz
from datetime import timedelta
from odoo.addons.website.controllers import form

from odoo.exceptions import AccessError, MissingError, UserError

_logger = logging.getLogger(__name__)


class BadmintooController(Survey):

    @route(['/my/badmintoo/assessment',
            '/my/badmintoo/assessment/page/<int:page>'], type='http', auth='user', website=True)
    def my_badmintoo_assessment(self, search=None, page=0, **kw):
        domain = []
        if search:
            domain.append(('name', 'ilike', search))
        org_domain = []
        if request.env.user.has_group(
                'organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        elif request.env.user.has_group(
                'organisation.group_organisation_coaches'):
            coach_ids = request.env['organisation.coaches'].search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            organisations = coach_ids.mapped('organisation_ids')
            org_domain.append(('id', 'in', organisations.ids))
        elif request.env.user.has_group(
                'organisation.group_organisation_athletes'):
            athlete_ids = request.env['organisation.athletes'].search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            organisations = athlete_ids.mapped('organisation_ids')
            org_domain.append(('id', 'in', organisations.ids))
        elif request.env.user.has_group(
                'organisation.group_organisation_parents'):
            parents = request.env['organisation.parents'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            organisations = parents.mapped('organisation_ids')
            org_domain.append(('id', 'in', organisations.ids))
        else:
            raise AccessError(
                _("Sorry you are not allowed to access this document"))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = None
        if org_domain:
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1)
            if organisation:
                domain.append(('organisation_id', '=', organisation.id))
        print(domain)
        assessments = request.env['badminto.assessment'].sudo().search(
            domain)
        customers = request.env['res.partner'].sudo().search(
            [('id', '!=', request.env.user.partner_id.id),
             ('organisation_ids', 'in', [organisation.id]),
             ('company_id', '=', request.env.user.company_id.id)])
        assessment_types = request.env['assessment.types'].sudo().search([])
        total = len(assessments)
        pager = request.website.pager(
            url='/my/registers',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        assessments = assessments[offset: offset + 6]
        # if request.env.user.has_group(
        #         'organisation.group_organisation_athletes'):
        print(assessments, "assessments")
        values = {
            'search': search,
            'assessments': assessments,
            'assessment_types': assessment_types,
            'total': total,
            'pager': pager,
            'is_account': True,
            'customers': customers
        }
        return request.render('badminto.assessment_template', values)

    @route(['/create/assessment'], type='http',
           auth='user', website=True)
    def create_badmintoo_assessment(self,  **post):
        print('create_badmintoo_assessment', post)
        customers = list(
            map(int, request.httprequest.form.getlist('customers')))
        type_ids = list(
            map(int, request.httprequest.form.getlist('assessment_types')))
        athletes = request.env['organisation.athletes'].sudo().search([('partner_id', 'in', customers)])
        organisation_id = request.env['organisation.organisation'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)])
        for rec in athletes:
            assessment = request.env['badminto.assessment'].sudo().create({
                'assessment_type_ids': [(4, type) for type in type_ids],
                'athlete_id': rec.id,
                'partner_id': rec.coach_ids.search([], limit=1).id,
                'organisation_id': organisation_id.id,
            })

        return request.redirect('/my/badmintoo/assessment')

    @http.route(['/my/assessment'],
                type='http',
                auth="user", website=True)
    def my_assessment_details(self, **post):
        if post.get('assessment'):
            print("pos", post.get('assessment'))
            assessment = request.env['badminto.assessment'].sudo().browse(
                int(post.get('assessment')))
            lifestyle_assessment_id = request.env[
                'ir.config_parameter'].sudo().get_param(
                'config.lifestyle_data_survey_id', 'False')
            # if lifestyle_assessment_id:
            lifestyle_assessment = request.env['survey.survey'].sudo().browse(
                int(lifestyle_assessment_id))
            hrv_assessment_id = request.env[
                'ir.config_parameter'].sudo().get_param(
                'config.hrv_data_survey_id', 'False')
            # if lifestyle_assessment_id:
            hrv_assessment = request.env['survey.survey'].sudo().browse(
                int(hrv_assessment_id))
            answers = lifestyle_assessment.user_input_ids.filtered(lambda
                                                                       x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
            hrv_answers = hrv_assessment.user_input_ids.filtered(lambda
                                                                       x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
            mobility_assessment_id = request.env[
                'ir.config_parameter'].sudo().get_param(
                'config.mobility_data_survey_id', 'False')
            # if lifestyle_assessment_id:
            mobility_assessment = request.env['survey.survey'].sudo().browse(
                int(mobility_assessment_id))
            mobility_answers = mobility_assessment.user_input_ids.filtered(lambda
                                                                     x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
            mental_assessment_id = request.env[
                'ir.config_parameter'].sudo().get_param(
                'config.mental_data_survey_id', 'False')
            # if lifestyle_assessment_id:
            mental_assessment = request.env['survey.survey'].sudo().browse(
                int(mental_assessment_id))
            mental_answers = mental_assessment.user_input_ids.filtered(
                lambda
                    x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
            sc_assessment_id = request.env[
                'ir.config_parameter'].sudo().get_param(
                'config.sc_data_survey_id', 'False')
            # if lifestyle_assessment_id:
            sc_assessment = request.env['survey.survey'].sudo().browse(
                int(sc_assessment_id))
            sc_answers = sc_assessment.user_input_ids.filtered(
                lambda
                    x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
            anaerobic_assessment_id = request.env[
                'ir.config_parameter'].sudo().get_param(
                'config.anaerobic_data_survey_id', 'False')
            # if lifestyle_assessment_id:
            anaerobic_assessment = request.env['survey.survey'].sudo().browse(
                int(anaerobic_assessment_id))
            anaerobic_answers = anaerobic_assessment.user_input_ids.filtered(
                lambda
                    x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
            aerobic_assessment_id = request.env[
                'ir.config_parameter'].sudo().get_param(
                'config.aerobic_data_survey_id', 'False')
            # if lifestyle_assessment_id:
            aerobic_assessment = request.env['survey.survey'].sudo().browse(
                int(aerobic_assessment_id))
            aerobic_answers = aerobic_assessment.user_input_ids.filtered(
                lambda
                    x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
            nutrition_assessment_id = request.env[
                'ir.config_parameter'].sudo().get_param(
                'config.nutrition_data_survey_id', 'False')
            # if lifestyle_assessment_id:
            nutrition_assessment = request.env['survey.survey'].sudo().browse(
                int(nutrition_assessment_id))
            nutrition_answers = nutrition_assessment.user_input_ids.filtered(
                lambda
                    x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')

            #UPDATED FOR COMPLETED VIDEO UPLOADS

            print('assesssment post', post)
            attachments = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'badminto.assessment'),
                ('res_id', '=', int(post.get('assessment'))),
                ('badminto_field_name', '!=', None)
            ])
            print('attachmentsss', attachments)
            print(len(attachments))
            badminto_fields = attachments.mapped(lambda x: x.badminto_field_name)
            print('fields names', badminto_fields)

            values = {
                'is_account': True,
                'assessment': assessment,
                'lifestyle_answers': answers,
                'hrv_answers': hrv_answers,
                'mobility_answers': mobility_answers,
                'mental_answers': mental_answers,
                'sc_answers': sc_answers,
                'anaerobic_answers': anaerobic_answers,
                'aerobic_answers': aerobic_answers,
                'nutrition_answers': nutrition_answers,
                'badminto_fields': badminto_fields
            }
            if 'service_video' in badminto_fields and 'receiving_video' in badminto_fields:
                values.update({
                    'sr_completed': True,
                })
            if 'fnz_co_fnp_video' in badminto_fields and 'fnz_co_ofcn_video' in badminto_fields and 'fnz_co_fol_video' in badminto_fields and 'fnz_co_fss_video' in badminto_fields and 'fnz_co_frs_video' in badminto_fields and 'fnz_co_nb_video' in badminto_fields and 'fnz_frs_video' in badminto_fields and 'fnz_neutralisation_video' in badminto_fields and 'fnz_cd_dfcn_video' in badminto_fields and 'fnz_cd_dfl_video' in badminto_fields and 'fnz_td_dd_video' in badminto_fields:
                values.update({
                    'fnz_completed': True,
                })
            if 'bnz_to_fnk_video' in badminto_fields and 'bnz_co_fnp_video' in badminto_fields and 'bnz_co_ofcn_video' in badminto_fields and 'bnz_co_fol_video' in badminto_fields and 'bnz_co_fss_video' in badminto_fields and 'bnz_co_frs_video' in badminto_fields and 'bnz_co_nb_video' in badminto_fields and 'bnz_frs_video' in badminto_fields and 'bnz_neutralisation_video' in badminto_fields and 'bnz_cd_dfcn_video' in badminto_fields and 'bnz_cd_dfl_video' in badminto_fields and 'bnz_td_dd_video' in badminto_fields:
                values.update({
                    'bnz_completed': True,
                })
            if 'fmz_co_ss_video' in badminto_fields and 'fmz_fmcp_video' in badminto_fields  and 'fmz_cd_fds_s_video' in badminto_fields and 'fmz_cd_fdc_s_video' in badminto_fields and 'fmz_cd_fds_l_video' in badminto_fields and 'fmz_cd_fdc_l_video' in badminto_fields and 'fmz_cd_fdca_video' in badminto_fields and 'fmz_fd_video' in badminto_fields:
                values.update({
                    'fmz_completed': True,
                })
            if 'bmz_co_ss_video' in badminto_fields and 'bmz_bmcp_video' in badminto_fields and 'bmz_cd_bds_s_video' in badminto_fields and 'bmz_cd_bdc_s_video' in badminto_fields and 'bmz_cd_bds_l_video' in badminto_fields and 'bmz_cd_bdc_l_video' in badminto_fields and 'bmz_cd_bdc_video' in badminto_fields and 'bmz_td_bd_video' in badminto_fields:
                values.update({
                    'bmz_completed': True,
                })
            if 'rcovhz_to_js_video' in badminto_fields and 'rcovhz_to_frs_video' in badminto_fields and 'rcovhz_to_co_ss_video' in badminto_fields and 'rcovhz_co_oc_video' in badminto_fields and 'rcovhz_co_orc_video' in badminto_fields and 'rcovhz_co_ooc_video' in badminto_fields and 'rcovhz_oc_video' in badminto_fields:
                values.update({
                    'rcovhz_completed': True,
                })
            if 'rcbz_co_obc_video' in badminto_fields and 'rcbz_co_brd_video' in badminto_fields and 'rcbz_bcd_video' in badminto_fields and 'rcbz_cd_ns_video' in badminto_fields and 'rcbz_cd_nc_video' in badminto_fields:
                print("rcbz")
                values.update({
                    'rcbz_completed': True,
                })
            if 'rcfz_to_js_video' in badminto_fields and 'rcfz_to_fbrs_video' in badminto_fields and 'rcfz_co_oc_video' in badminto_fields and 'rcfz_co_fcs_video' in badminto_fields and 'rcfz_co_fcc_video' in badminto_fields and 'rcfz_co_fnd_video' in badminto_fields and 'rcfz_co_frcs_video' in badminto_fields and 'rcfz_co_dc_video' in badminto_fields and 'rcfz_fn_video' in badminto_fields and 'rcfz_td_fd_video' in badminto_fields:
                values.update({
                    'rcfz_completed': True,
                })
            if 'footwork_ofp_video' in badminto_fields and 'footwork_dfp_video' in badminto_fields:
                values.update({
                    'footwork_completed': True,
                })
            return request.render('badminto.assessment_details_template',
                                  values)

    @http.route(['/my/general/assessment/lifestyle'],
                type='http',
                auth="user", website=True)
    def my_lifestyle_assessment(self, answer_token=False,email=False, **post):
        print(post, "lifestyle")
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment')))
        print(assessment.athlete_id.partner_id.country_id.image_url,
              "image")
        lifestyle_assessment_id = request.env['ir.config_parameter'].sudo().get_param('config.lifestyle_data_survey_id', 'False')
        # if lifestyle_assessment_id:
        lifestyle_assessment = request.env['survey.survey'].sudo().browse(int(lifestyle_assessment_id))
        survey_start_url = werkzeug.urls.url_join(
            lifestyle_assessment.get_base_url(),
            lifestyle_assessment.get_start_url()) if lifestyle_assessment else False
        print(survey_start_url)

        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get(
                'survey_%s' % lifestyle_assessment.access_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(lifestyle_assessment.access_token, answer_token,
                                            ensure_token=False)

        if answer_from_cookie and access_data['validity_code'] in (
        'answer_wrong_user', 'token_wrong'):
            # If the cookie had been generated for another user or does not correspond to any existing answer object
            # (probably because it has been deleted), ignore it and redo the check.
            # The cookie will be replaced by a legit value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(lifestyle_assessment.access_token, None,
                                                ensure_token=False)

        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data,
                                             access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
            'answer_sudo']
        if not answer_sudo:
            try:
                answer_sudo = survey_sudo._create_answer(user=request.env.user,
                                                         email=email)
            except UserError:
                answer_sudo = False
        answer_from_cookie = False
        answers = lifestyle_assessment.user_input_ids.filtered(lambda x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
        print("answer_from_cookie", answers)
        # if not answer_token:
        #     answer_token = request.httprequest.cookies.get(
        #         'survey_%s' % lifestyle_assessment.access_token)
        #     answer_from_cookie = bool(answer_token)
        #     print(answer_from_cookie,request.httprequest.cookies, lifestyle_assessment.access_token, answer_token)
        #
        # access_data = self._get_access_data(lifestyle_assessment.access_token, answer_token,
        #                                     ensure_token=False)
        # print(self._prepare_survey_data(
        #                           access_data['survey_sudo'], access_data['answer_sudo'],
        #                           **post))


        values = {
            'is_account': True,
            'assessment': assessment,
            'lifestyle_assessment': lifestyle_assessment,
            'survey': lifestyle_assessment,
            'answer': answer_sudo,
            'answer_complete': True if answers else False,

        }
        if not answers:
            return request.render('badminto.lifestyle_assessment_details_template', values)
        else:
            for rec in answers:
                return request.redirect('/survey/print/%s?answer_token=%s&amp;review=True' % (lifestyle_assessment.access_token, rec.access_token))

    @http.route(['/my/general/assessment/hr/hrv'],
                type='http',
                auth="user", website=True)
    def my_hr_hrv_assessment(self, answer_token=False, email=False,
                                **post):
        print(post, "lifestyle")
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment')))
        #
        hrv_assessment = request.env[
            'ir.config_parameter'].sudo().get_param(
            'config.hrv_data_survey_id', 'False')
        print(hrv_assessment, "lifestyle")

        # # if lifestyle_assessment_id:
        hrv_assessment_id = request.env['survey.survey'].sudo().browse(
            int(hrv_assessment))
        # survey_start_url = werkzeug.urls.url_join(
        #     hrv_assessment.get_base_url(),
        #     hrv_assessment.get_start_url()) if hrv_assessment else False
        # print(survey_start_url)
        #
        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get(
                'survey_%s' % hrv_assessment_id.access_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(
            hrv_assessment_id.access_token, answer_token,
            ensure_token=False)

        if answer_from_cookie and access_data['validity_code'] in (
                'answer_wrong_user', 'token_wrong'):
            # If the cookie had been generated for another user or does not correspond to any existing answer object
            # (probably because it has been deleted), ignore it and redo the check.
            # The cookie will be replaced by a legit value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(
                hrv_assessment_id.access_token, None,
                ensure_token=False)

        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data,
                                             access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
            'answer_sudo']
        if not answer_sudo:
            try:
                answer_sudo = survey_sudo._create_answer(
                    user=request.env.user,
                    email=email)
            except UserError:
                answer_sudo = False
        answer_from_cookie = False
        answers = hrv_assessment_id.user_input_ids.filtered(lambda
                                                                   x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
        print("answer_from_cookie", answers)
        # if not answer_token:
        #     answer_token = request.httprequest.cookies.get(
        #         'survey_%s' % lifestyle_assessment.access_token)
        #     answer_from_cookie = bool(answer_token)
        #     print(answer_from_cookie,request.httprequest.cookies, lifestyle_assessment.access_token, answer_token)
        #
        # access_data = self._get_access_data(lifestyle_assessment.access_token, answer_token,
        #                                     ensure_token=False)
        # print(self._prepare_survey_data(
        #                           access_data['survey_sudo'], access_data['answer_sudo'],
        #                           **post))

        values = {
            'is_account': True,
            'assessment': assessment,
            'hrv_assessment': hrv_assessment_id,
            'survey': hrv_assessment_id,
            'answer': answer_sudo,
            'answer_complete': True if answers else False,

        }
        if not answers:
            return request.render(
                'badminto.hrv_assessment_details_template', values)
        else:
            for rec in answers:
                return request.redirect(
                    '/survey/print/%s?answer_token=%s&amp;review=True' % (
                    hrv_assessment_id.access_token, rec.access_token))

    @http.route(['/my/general/assessment/mobility'],
                type='http',
                auth="user", website=True)
    def my_mobility_assessment(self, answer_token=False, email=False, **post):
        print(post, "lifestyle")
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment')))
        mobility_assessment_id = request.env[
            'ir.config_parameter'].sudo().get_param(
            'config.mobility_data_survey_id', 'False')
        # if lifestyle_assessment_id:
        mobility_assessment = request.env['survey.survey'].sudo().browse(
            int(mobility_assessment_id))
        survey_start_url = werkzeug.urls.url_join(
            mobility_assessment.get_base_url(),
            mobility_assessment.get_start_url()) if mobility_assessment else False
        print(survey_start_url)

        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get(
                'survey_%s' % mobility_assessment.access_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(mobility_assessment.access_token,
                                            answer_token,
                                            ensure_token=False)

        if answer_from_cookie and access_data['validity_code'] in (
                'answer_wrong_user', 'token_wrong'):
            # If the cookie had been generated for another user or does not correspond to any existing answer object
            # (probably because it has been deleted), ignore it and redo the check.
            # The cookie will be replaced by a legit value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(
                mobility_assessment.access_token, None,
                ensure_token=False)

        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data,
                                             access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
            'answer_sudo']
        if not answer_sudo:
            try:
                answer_sudo = survey_sudo._create_answer(user=request.env.user,
                                                         email=email)
            except UserError:
                answer_sudo = False
        answer_from_cookie = False
        answers = mobility_assessment.user_input_ids.filtered(lambda
                                                                   x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
        print("answer_from_cookie", answers)
        # if not answer_token:
        #     answer_token = request.httprequest.cookies.get(
        #         'survey_%s' % lifestyle_assessment.access_token)
        #     answer_from_cookie = bool(answer_token)
        #     print(answer_from_cookie,request.httprequest.cookies, lifestyle_assessment.access_token, answer_token)
        #
        # access_data = self._get_access_data(lifestyle_assessment.access_token, answer_token,
        #                                     ensure_token=False)
        # print(self._prepare_survey_data(
        #                           access_data['survey_sudo'], access_data['answer_sudo'],
        #                           **post))

        values = {
            'is_account': True,
            'assessment': assessment,
            'mobility_assessment': mobility_assessment,
            'survey': mobility_assessment,
            'answer': answer_sudo,
            'answer_complete': True if answers else False,

        }
        if not answers:
            return request.render(
                'badminto.mobility_assessment_details_template', values)
        else:
            for rec in answers:
                return request.redirect(
                    '/survey/print/%s?answer_token=%s&amp;review=True' % (
                    mobility_assessment.access_token, rec.access_token))

    @http.route(['/my/general/assessment/mental'],
                type='http',
                auth="user", website=True)
    def my_mental_assessment(self, answer_token=False, email=False, **post):
        print(post, "lifestyle")
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment')))

        mental_assessment_id = request.env[
            'ir.config_parameter'].sudo().get_param(
            'config.mental_data_survey_id', 'False')
        # if lifestyle_assessment_id:
        mental_assessment = request.env['survey.survey'].sudo().browse(
            int(mental_assessment_id))
        survey_start_url = werkzeug.urls.url_join(
            mental_assessment.get_base_url(),
            mental_assessment.get_start_url()) if mental_assessment else False
        print(survey_start_url)

        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get(
                'survey_%s' % mental_assessment.access_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(mental_assessment.access_token,
                                            answer_token,
                                            ensure_token=False)

        if answer_from_cookie and access_data['validity_code'] in (
                'answer_wrong_user', 'token_wrong'):
            # If the cookie had been generated for another user or does not correspond to any existing answer object
            # (probably because it has been deleted), ignore it and redo the check.
            # The cookie will be replaced by a legit value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(
                mental_assessment.access_token, None,
                ensure_token=False)

        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data,
                                             access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
            'answer_sudo']
        if not answer_sudo:
            try:
                answer_sudo = survey_sudo._create_answer(user=request.env.user,
                                                         email=email)
            except UserError:
                answer_sudo = False
        answer_from_cookie = False
        answers = mental_assessment.user_input_ids.filtered(lambda
                                                                   x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
        print("answer_from_cookie", answers)
        # if not answer_token:
        #     answer_token = request.httprequest.cookies.get(
        #         'survey_%s' % lifestyle_assessment.access_token)
        #     answer_from_cookie = bool(answer_token)
        #     print(answer_from_cookie,request.httprequest.cookies, lifestyle_assessment.access_token, answer_token)
        #
        # access_data = self._get_access_data(lifestyle_assessment.access_token, answer_token,
        #                                     ensure_token=False)
        # print(self._prepare_survey_data(
        #                           access_data['survey_sudo'], access_data['answer_sudo'],
        #                           **post))

        values = {
            'is_account': True,
            'assessment': assessment,
            'mental_assessment': mental_assessment,
            'survey': mental_assessment,
            'answer': answer_sudo,
            'answer_complete': True if answers else False,

        }
        if not answers:
            return request.render(
                'badminto.mental_assessment_details_template', values)
        else:
            for rec in answers:
                return request.redirect(
                    '/survey/print/%s?answer_token=%s&amp;review=True' % (
                    mental_assessment.access_token, rec.access_token))

    @http.route(['/my/general/assessment/sc'],
                type='http',
                auth="user", website=True)
    def my_sc_assessment(self, answer_token=False, email=False, **post):
        print(post, "lifestyle")
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment')))

        sc_assessment_id = request.env[
            'ir.config_parameter'].sudo().get_param(
            'config.sc_data_survey_id', 'False')
        # if lifestyle_assessment_id:
        sc_assessment = request.env['survey.survey'].sudo().browse(
            int(sc_assessment_id))
        survey_start_url = werkzeug.urls.url_join(
            sc_assessment.get_base_url(),
            sc_assessment.get_start_url()) if sc_assessment else False
        print(survey_start_url)

        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get(
                'survey_%s' % sc_assessment.access_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(sc_assessment.access_token,
                                            answer_token,
                                            ensure_token=False)

        if answer_from_cookie and access_data['validity_code'] in (
                'answer_wrong_user', 'token_wrong'):
            # If the cookie had been generated for another user or does not correspond to any existing answer object
            # (probably because it has been deleted), ignore it and redo the check.
            # The cookie will be replaced by a legit value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(
                sc_assessment.access_token, None,
                ensure_token=False)

        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data,
                                             access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
            'answer_sudo']
        if not answer_sudo:
            try:
                answer_sudo = survey_sudo._create_answer(user=request.env.user,
                                                         email=email)
            except UserError:
                answer_sudo = False
        answer_from_cookie = False
        answers = sc_assessment.user_input_ids.filtered(lambda
                                                                x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
        print("answer_from_cookie", answers)
        # if not answer_token:
        #     answer_token = request.httprequest.cookies.get(
        #         'survey_%s' % lifestyle_assessment.access_token)
        #     answer_from_cookie = bool(answer_token)
        #     print(answer_from_cookie,request.httprequest.cookies, lifestyle_assessment.access_token, answer_token)
        #
        # access_data = self._get_access_data(lifestyle_assessment.access_token, answer_token,
        #                                     ensure_token=False)
        # print(self._prepare_survey_data(
        #                           access_data['survey_sudo'], access_data['answer_sudo'],
        #                           **post))

        values = {
            'is_account': True,
            'assessment': assessment,
            'sc_assessment': sc_assessment,
            'survey': sc_assessment,
            'answer': answer_sudo,
            'answer_complete': True if answers else False,

        }
        if not answers:
            return request.render(
                'badminto.sc_assessment_details_template', values)
        else:
            for rec in answers:
                return request.redirect(
                    '/survey/print/%s?answer_token=%s&amp;review=True' % (
                        sc_assessment.access_token, rec.access_token))

    @http.route(['/my/general/assessment/aerobic'],
                type='http',
                auth="user", website=True)
    def my_aerobic_assessment(self, answer_token=False, email=False, **post):
        print(post, "lifestyle")
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment')))

        aerobic_assessment_id = request.env[
            'ir.config_parameter'].sudo().get_param(
            'config.aerobic_data_survey_id', 'False')
        # if lifestyle_assessment_id:
        aerobic_assessment = request.env['survey.survey'].sudo().browse(
            int(aerobic_assessment_id))
        survey_start_url = werkzeug.urls.url_join(
            aerobic_assessment.get_base_url(),
            aerobic_assessment.get_start_url()) if aerobic_assessment else False
        print(survey_start_url)

        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get(
                'survey_%s' % aerobic_assessment.access_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(aerobic_assessment.access_token,
                                            answer_token,
                                            ensure_token=False)

        if answer_from_cookie and access_data['validity_code'] in (
                'answer_wrong_user', 'token_wrong'):
            # If the cookie had been generated for another user or does not correspond to any existing answer object
            # (probably because it has been deleted), ignore it and redo the check.
            # The cookie will be replaced by a legit value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(
                aerobic_assessment.access_token, None,
                ensure_token=False)

        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data,
                                             access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
            'answer_sudo']
        if not answer_sudo:
            try:
                answer_sudo = survey_sudo._create_answer(user=request.env.user,
                                                         email=email)
            except UserError:
                answer_sudo = False
        answer_from_cookie = False
        answers = aerobic_assessment.user_input_ids.filtered(lambda
                                                            x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
        print("answer_from_cookie", answers)
        # if not answer_token:
        #     answer_token = request.httprequest.cookies.get(
        #         'survey_%s' % lifestyle_assessment.access_token)
        #     answer_from_cookie = bool(answer_token)
        #     print(answer_from_cookie,request.httprequest.cookies, lifestyle_assessment.access_token, answer_token)
        #
        # access_data = self._get_access_data(lifestyle_assessment.access_token, answer_token,
        #                                     ensure_token=False)
        # print(self._prepare_survey_data(
        #                           access_data['survey_sudo'], access_data['answer_sudo'],
        #                           **post))

        values = {
            'is_account': True,
            'assessment': assessment,
            'aerobic_assessment': aerobic_assessment,
            'survey': aerobic_assessment,
            'answer': answer_sudo,
            'answer_complete': True if answers else False,

        }
        if not answers:
            return request.render(
                'badminto.aerobic_assessment_details_template', values)
        else:
            for rec in answers:
                return request.redirect(
                    '/survey/print/%s?answer_token=%s&amp;review=True' % (
                        aerobic_assessment.access_token, rec.access_token))

    @http.route(['/my/general/assessment/anaerobic'],
                type='http',
                auth="user", website=True)
    def my_anaerobic_assessment(self, answer_token=False, email=False, **post):
        print(post, "lifestyle")
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment')))

        anaerobic_assessment_id = request.env[
            'ir.config_parameter'].sudo().get_param(
            'config.anaerobic_data_survey_id', 'False')
        # if lifestyle_assessment_id:
        anaerobic_assessment = request.env['survey.survey'].sudo().browse(
            int(anaerobic_assessment_id))
        survey_start_url = werkzeug.urls.url_join(
            anaerobic_assessment.get_base_url(),
            anaerobic_assessment.get_start_url()) if anaerobic_assessment else False
        print(survey_start_url)

        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get(
                'survey_%s' % anaerobic_assessment.access_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(anaerobic_assessment.access_token,
                                            answer_token,
                                            ensure_token=False)

        if answer_from_cookie and access_data['validity_code'] in (
                'answer_wrong_user', 'token_wrong'):
            # If the cookie had been generated for another user or does not correspond to any existing answer object
            # (probably because it has been deleted), ignore it and redo the check.
            # The cookie will be replaced by a legit value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(
                anaerobic_assessment.access_token, None,
                ensure_token=False)

        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data,
                                             access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
            'answer_sudo']
        if not answer_sudo:
            try:
                answer_sudo = survey_sudo._create_answer(user=request.env.user,
                                                         email=email)
            except UserError:
                answer_sudo = False
        answer_from_cookie = False
        answers = anaerobic_assessment.user_input_ids.filtered(lambda
                                                            x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
        print("answer_from_cookie", answers)
        # if not answer_token:
        #     answer_token = request.httprequest.cookies.get(
        #         'survey_%s' % lifestyle_assessment.access_token)
        #     answer_from_cookie = bool(answer_token)
        #     print(answer_from_cookie,request.httprequest.cookies, lifestyle_assessment.access_token, answer_token)
        #
        # access_data = self._get_access_data(lifestyle_assessment.access_token, answer_token,
        #                                     ensure_token=False)
        # print(self._prepare_survey_data(
        #                           access_data['survey_sudo'], access_data['answer_sudo'],
        #                           **post))

        values = {
            'is_account': True,
            'assessment': assessment,
            'anaerobic_assessment': anaerobic_assessment,
            'survey': anaerobic_assessment,
            'answer': answer_sudo,
            'answer_complete': True if answers else False,

        }
        if not answers:
            return request.render(
                'badminto.anaerobic_assessment_details_template', values)
        else:
            for rec in answers:
                return request.redirect(
                    '/survey/print/%s?answer_token=%s&amp;review=True' % (
                        anaerobic_assessment.access_token, rec.access_token))

    @http.route(['/my/general/assessment/nutrition'],
                type='http',
                auth="user", website=True)
    def my_nutrition_assessment(self, answer_token=False, email=False, **post):
        print(post, "lifestyle")
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(post.get('assessment')))

        nutrition_assessment_id = request.env[
            'ir.config_parameter'].sudo().get_param(
            'config.nutrition_data_survey_id', 'False')
        # if lifestyle_assessment_id:
        nutrition_assessment = request.env['survey.survey'].sudo().browse(
            int(nutrition_assessment_id))
        survey_start_url = werkzeug.urls.url_join(
            nutrition_assessment.get_base_url(),
            nutrition_assessment.get_start_url()) if nutrition_assessment_id else False
        print(survey_start_url)

        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get(
                'survey_%s' % nutrition_assessment.access_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(nutrition_assessment.access_token,
                                            answer_token,
                                            ensure_token=False)

        if answer_from_cookie and access_data['validity_code'] in (
                'answer_wrong_user', 'token_wrong'):
            # If the cookie had been generated for another user or does not correspond to any existing answer object
            # (probably because it has been deleted), ignore it and redo the check.
            # The cookie will be replaced by a legit value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(
                nutrition_assessment.access_token, None,
                ensure_token=False)

        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data,
                                             access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
            'answer_sudo']
        if not answer_sudo:
            try:
                answer_sudo = survey_sudo._create_answer(user=request.env.user,
                                                         email=email)
            except UserError:
                answer_sudo = False
        answer_from_cookie = False
        answers = nutrition_assessment.user_input_ids.filtered(lambda
                                                                   x: x.partner_id.id == request.env.user.partner_id.id and x.state == 'done')
        print("answer_from_cookie", answers)
        # if not answer_token:
        #     answer_token = request.httprequest.cookies.get(
        #         'survey_%s' % lifestyle_assessment.access_token)
        #     answer_from_cookie = bool(answer_token)
        #     print(answer_from_cookie,request.httprequest.cookies, lifestyle_assessment.access_token, answer_token)
        #
        # access_data = self._get_access_data(lifestyle_assessment.access_token, answer_token,
        #                                     ensure_token=False)
        # print(self._prepare_survey_data(
        #                           access_data['survey_sudo'], access_data['answer_sudo'],
        #                           **post))

        values = {
            'is_account': True,
            'assessment': assessment,
            'nutrition_assessment': nutrition_assessment,
            'survey': nutrition_assessment,
            'answer': answer_sudo,
            'answer_complete': True if answers else False,

        }
        if not answers:
            return request.render(
                'badminto.nutrition_assessment_details_template', values)
        else:
            for rec in answers:
                return request.redirect(
                    '/survey/print/%s?answer_token=%s&amp;review=True' % (
                    nutrition_assessment.access_token, rec.access_token))

