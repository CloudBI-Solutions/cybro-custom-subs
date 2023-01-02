
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
        print('pooos', post)
        if post.get('assessment'):
            assessment = request.env['badminto.assessment'].sudo().browse(
                int(post.get('assessment')))
            lifestyle_assessment_id = request.env[
                'ir.config_parameter'].sudo().get_param(
                'config.lifestyle_data_survey_id', 'False')
            # if lifestyle_assessment_id:
            lifestyle_assessment = request.env['survey.survey'].sudo().browse(
                int(lifestyle_assessment_id))
            answers = lifestyle_assessment.user_input_ids.filtered(
                lambda x: x.partner_id.id == request.env.user.partner_id.id and
                          x.state == 'done')
            values = {
                'is_account': True,
                'assessment': assessment,
                'answers': answers
            }
            return request.render('badminto.assessment_details_template', values)

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