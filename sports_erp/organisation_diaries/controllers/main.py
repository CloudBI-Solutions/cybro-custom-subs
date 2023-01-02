import json
import logging
import werkzeug

_logger = logging.getLogger(__name__)

from odoo import fields, http, _
from odoo.addons.survey.controllers.main import Survey
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo import http
from odoo.http import request
import base64
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager
from odoo.exceptions import AccessError, MissingError, UserError
from odoo.tools import format_datetime, format_date, is_html_empty
from odoo.http import content_disposition, dispatch_rpc, request, \
    serialize_exception


class SurveyDiaries(Survey):

    @http.route('/survey/calculated_metric', type='json', auth='public',
                website=True)
    def survey_calculated_metric(self, **kwargs):
        if kwargs.get('question_id'):
            survey_question = request.env['survey.question'].sudo().search([
                ('id', '=', int(kwargs.get('question_id')))])
            print(survey_question.survey_id.question_and_page_ids.filtered(
                lambda x:x.question_type == 'calculated_metric'), "survey_question")
            # answers = {}
            # for question in survey_question.survey_id.question_and_page_ids.filtered(
            #     lambda x:x.question_type == 'calculated_metric'):
            #     for metric in question.calculated_metric_ids.filtered(
            #             lambda x: x.operand_1.id in survey_question.calculated_metric_ids.ids or x.operand_2.id in survey_question.calculated_metric_ids.ids):
            #         if metric.operator.type == 'multiply':
            #             if metric.operand_1.id in survey_question.calculated_metric_ids.ids:
            #
            #                 answers.update({
            #                     'question': question.id,
            #                     # 'answer': answer
            #                 })
            #                 print(metric, "metric")
            # if survey_question.calculated_metric_ids:
            #     for metric in survey_question.calculated_metric_ids:
            #         print(metric, "metric")


