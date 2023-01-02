
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


class BadmintooAssessmentController(http.Controller):

    @route(['/my/badmintoo/assessment/plans',
            '/my/badmintoo/assessment/plans/page/<int:page>'],
           type='http', auth='user', website=True)
    def my_badmintoo_assessment_plans(self, search=None, page=0, **kw):
        print("Assessment Plans")
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
        assessments_plans = request.env['assessment.plan'].sudo().search(
            domain)
        # customers = request.env['res.partner'].sudo().search(
        #     [('id', '!=', request.env.user.partner_id.id),
        #      ('organisation_ids', 'in', [organisation.id]),
        #      ('company_id', '=', request.env.user.company_id.id)])
        assessment_types = request.env['assessment.types'].sudo().search([])
        total = len(assessments_plans)
        pager = request.website.pager(
            url='/my/badmintoo/assessment/plans',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        assessments_plans = assessments_plans[offset: offset + 6]
        # if request.env.user.has_group(
        #         'organisation.group_organisation_athletes'):
        print(assessments_plans, "assessments")
        values = {
            'search': search,
            'assessments_plans': assessments_plans,
            'assessment_types': assessment_types,
            'total': total,
            'pager': pager,
            'taxes': request.env['account.tax'].sudo().search([]),
            'is_account': True,
        }
        return request.render('badminto.assessment_plans_template', values)

    @route(['/create/assessment_plan'],
           type='http', auth='user', website=True)
    def create_assessment_plan(self, **post):
        organisation_id = request.env[
            'organisation.organisation'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)])
        print('org_id', organisation_id)
        assessment_types = list(
            map(int, request.httprequest.form.getlist('assessment_types')))
        taxes = list(map(int, request.httprequest.form.getlist('')))
        assessment_plan = request.env['assessment.plan'].sudo().create({
            'name': post.get('name'),
            'price': post.get('price'),
            'assessment_type_ids': [(4, type) for type in assessment_types],
            'tax_ids': [(4, int(post.get('taxes')))] if post.get('taxes') else False,
            'organisation_id': organisation_id.id,
        })
        assessment_plan.product_id.write({
            'is_published': True if post.get(
                'available_in_front_end') == 'on' else False,
        })
        return request.redirect('/my/badmintoo/assessment/plans')

    @route(['/update/assessment_configuration'],
           type='http', auth='user', website=True)
    def update_assessment_configuration(self, **post):
        print(post)
        organisation_id = request.env[
            'organisation.organisation'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)])
        print('organisation', organisation_id)

        if post.get('lifestyle_assessment'):
            organisation_id.update({
                'lifestyle_assessment_data_id': int(
                    post.get('lifestyle_assessment'))
            })

        if post.get('s_c_assessment'):
            organisation_id.update({
                'sc_assessment_data_id': int(
                    post.get('s_c_assessment'))
            })

        if post.get('mobility_assessment'):
            organisation_id.update({
                'mobility_assessment_data_id': int(
                    post.get('mobility_assessment'))
            })

        if post.get('mental_assessment'):
            organisation_id.update({
                'mental_assessment_data_id': int(
                    post.get('mental_assessment'))
            })

        if post.get('hrv_assessment'):
            organisation_id.update({
                'hrv_assessment_data_id': int(
                    post.get('hrv_assessment'))
            })

        if post.get('nutrition_assessment'):
            organisation_id.update({
                'nutrition_assessment_data_id': int(
                    post.get('nutrition_assessment'))
            })

        if post.get('aerobic_assessment'):
            organisation_id.update({
                'aerobic_assessment_data_id': int(
                    post.get('aerobic_assessment'))
            })

        if post.get('anaerobic_assessment'):
            organisation_id.update({
                'anaerobic_assessment_data_id': int(
                    post.get('anaerobic_assessment'))
            })
        return request.redirect('/my/badmintoo/assessment')
