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


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'survey_count' in counters:
            partner = request.env.user.partner_id
            values['survey_count'] = request.env[
                'survey.user_input'].sudo().search_count([
                ('partner_id', '=', partner.id)
            ])
        return values

    @http.route(['/my/surveys', '/my/surveys/page/<int:page>'], type='http',
                auth="user", website=True)
    def portal_my_surveys(self, page=1, date_begin=None, date_end=None,
                          sortby=None, filterby=None, search=None,
                          search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        Survey = request.env['survey.user_input']
        domain = [('partner_id', '=', partner.id), ]
        # ('parent_id', 'in', [None, False, []])

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'display_name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]

        # projects count
        survey_count = Survey.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/surveys",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby},
            total=survey_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        surveys = Survey.sudo().search(domain, order=order,
                                       limit=self._items_per_page,
                                       offset=pager['offset'])
        request.session['my_surveys_history'] = surveys.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'surveys': surveys,
            'page_name': 'surveys',
            'default_url': '/my/surveys',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("survey_extension.portal_my_surveys", values)

    @http.route(['/my/survey/<int:survey_id>'], type='http', auth="public",
                website=True)
    def portal_my_survey(self, survey_id=None, access_token=None, **kw):
        try:
            survey_sudo = self._document_check_access('survey.user_input',
                                                      survey_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._survey_get_page_view_values(survey_sudo, access_token,
                                                   **kw)
        # send_application_msg = False
        # if values.get('child_id', False):
        #     # send_application_msg = str(any([x.state != 'done' for x in values.get('child_id')]))
        #     send_application_msg = str(not all([x.is_final_submit for x in values.get('child_id')]))
        # values.update({
        #     'send_application_msg': str(send_application_msg).lower()
        # })
        print(">>>>>>>>>>>>>>>>>valuesvaluesvaluesvalues", values)
        return request.render("survey_extension.portal_my_survey", values)

    def _survey_get_page_view_values(self, survey, access_token, **kwargs):
        values = {
            'page_name': 'survey',
            'answer': survey,
            # 'child_id': survey.child_id
        }
        return self._get_page_view_values(survey, access_token, values,
                                          'my_surveys_history', False, **kwargs)

    # @http.route('/web/binary/download_document', type='http', auth="public")
    # def download_document(self, model, id, filename=None, **kw):
    #     """ Download link for files stored as binary fields.
    #     :param str model: name of the model to fetch the binary from
    #     :param str field: binary field
    #     :param str id: id of the record from which to fetch the binary
    #     :param str filename: field holding the file's name, if any
    #     :returns: :class:`werkzeug.wrappers.Response`
    #     """
    #     record = request.env[model].sudo().browse(int(id))
    #     if model == 'ir.attachment':
    #         binary_file = record.datas  # aqui colocas el nombre del campo binario que almacena tu archivo
    #     elif model == 'survey.user_input.line':
    #         binary_file = record.value_file
    #
    #     filecontent = base64.b64decode(binary_file or '')
    #
    #     content_type, disposition_content = False, False
    #
    #     if not filecontent:
    #         return request.not_found()
    #     else:
    #         if not filename:
    #             filename = '%s_%s' % (model.replace('.', '_'), id)
    #         content_type = ('Content-Type', 'application/octet-stream')
    #         disposition_content = ('Content-Disposition', content_disposition(filename))
    #
    #     return request.make_response(filecontent, [content_type,
    #                                                disposition_content])

    @http.route(
        '/survey/download/<string:answer_id>/<string:question_id>/<string:answer_token>',
        type='http',
        auth='public', website=True)
    def survey_download_file(self, **post):
        base_url = request.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        download_url = base_url
        print('>>>>>>>>>>>>>>>>', post.get('answer_id'),
              post.get('question_id'), post.get('answer_token'))
        if base_url and post.get('answer_id') and post.get(
                'question_id') and post.get('answer_token'):
            input_line_id = request.env['survey.user_input.line'].sudo().search(
                [('user_input_id.access_token', '=', post.get(
                    'answer_token')),
                 ('question_id', '=', int(post.get('question_id'))),
                 ('user_input_id', '=', int(post.get('answer_id')))], limit=1)
            if input_line_id:
                download_url += '/web/content/survey.user_input.line/' + \
                                str(input_line_id.id) + '/value_file?download=true'
        print('>>>download_url>>>', download_url)
        return request.redirect(download_url)

    # def binary_content(self, id, env=None, field='datas', share_id=None, share_token=None,
    #                    download=False, unique=False, filename_field='name'):
    #     env = env or request.env
    #     record = env['documents.document'].browse(int(id))
    #     filehash = None
    #
    #     if share_id:
    #         share = env['documents.share'].sudo().browse(int(share_id))
    #         record = share._get_documents_and_check_access(share_token, [int(id)], operation='read')
    #     if not record:
    #         return (404, [], None)
    #
    #     # check access right
    #     try:
    #         last_update = record['__last_update']
    #     except AccessError:
    #         return (404, [], None)
    #
    #     mimetype = False
    #     if record.type == 'url' and record.url:
    #         module_resource_path = record.url
    #         filename = os.path.basename(module_resource_path)
    #         status = 301
    #         content = module_resource_path
    #     else:
    #         status, content, filename, mimetype, filehash = env['ir.http']._binary_record_content(
    #             record, field=field, filename=None, filename_field=filename_field,
    #             default_mimetype='application/octet-stream')
    #     status, headers, content = env['ir.http']._binary_set_headers(
    #         status, content, filename, mimetype, unique, filehash=filehash, download=download)
    #
    #     return status, headers, content

    def _get_file_response(self, id, field='value_file', share_id=None,
                           share_token=None):
        """
        returns the http response to download one file.

        """

        # status, headers, content = self.binary_content(
        #     id, field=field, share_id=share_id, share_token=share_token, download=False,filename_field='file_name')

        status, content, filename, mimetype, filehash = request.env[
            'ir.http']._binary_record_content(
            id, field=field, filename=None, filename_field='file_name',
            default_mimetype='application/octet-stream')

        status, headers, content = request.env['ir.http']._binary_set_headers(
            status, content, filename, mimetype, unique=False,
            filehash=filehash, download=False)

        if status != 200:
            return request.env['ir.http']._response_by_status(status, headers,
                                                              content)
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            response = request.make_response(content_base64, headers)

        return response

    @http.route([
                    '/documents/content/preview/<string:answer_id>/<string:question_id>/<string:answer_token>'],
                type='http', auth='user')
    def documents_content(self, **post):
        if post.get('answer_id') and post.get('question_id') and post.get(
                'answer_token'):
            input_line_id = request.env['survey.user_input.line'].sudo().search(
                [('user_input_id.access_token', '=', post.get(
                    'answer_token')),
                 ('question_id', '=', int(post.get('question_id'))),
                 ('user_input_id', '=', int(post.get('answer_id')))], limit=1)
            return self._get_file_response(input_line_id)
        return False


class CustomSurvey(Survey):

    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        """ This method prepares all the data needed for template rendering, in function of the survey user input state.
            :param post:
                - previous_page_id : come from the breadcrumb or the back button and force the next questions to load
                                     to be the previous ones. """

        data = {
            'is_html_empty': is_html_empty,
            'survey': survey_sudo,
            'answer': answer_sudo,
            'breadcrumb_pages': [{
                'id': page.id,
                'title': page.title,
            } for page in survey_sudo.page_ids],
            'format_datetime': lambda dt: format_datetime(request.env, dt,
                                                          dt_format=False),
            'format_date': lambda date: format_date(request.env, date)
        }
        # From HERE !!!!!
        #         print('data', data)
        if survey_sudo.questions_layout != 'page_per_question':
            triggering_answer_by_question, triggered_questions_by_answer, selected_answers = answer_sudo._get_conditional_values()
            data.update({
                'triggering_answer_by_question': {
                    question.id: triggering_answer_by_question[question].id for
                    question in triggering_answer_by_question.keys()
                    if triggering_answer_by_question[question]
                },
                'triggered_questions_by_answer': {
                    answer.id: triggered_questions_by_answer[answer].ids
                    for answer in triggered_questions_by_answer.keys()
                },
                'selected_answers': selected_answers.ids
            })

        if not answer_sudo.is_session_answer and survey_sudo.is_time_limited and answer_sudo.start_datetime:
            data.update({
                'timer_start': answer_sudo.start_datetime.isoformat(),
                'time_limit_minutes': survey_sudo.time_limit
            })

        page_or_question_key = 'question' if survey_sudo.questions_layout == 'page_per_question' else 'page'

        # print('page_or_question', page_or_question_key)
        # print('post', post)

        # Bypass all if page_id is specified (comes from breadcrumb or previous button)
        if 'previous_page_id' in post:
            previous_page_or_question_id = int(post['previous_page_id'])
            new_previous_id = survey_sudo._get_next_page_or_question(
                answer_sudo, previous_page_or_question_id, go_back=True).id
            page_or_question = request.env['survey.question'].sudo().browse(
                previous_page_or_question_id)
            data.update({
                page_or_question_key: page_or_question,
                'previous_page_id': new_previous_id,
                'has_answered': answer_sudo.user_input_line_ids.filtered(
                    lambda line: line.question_id.id == new_previous_id),
                'can_go_back': survey_sudo._can_go_back(answer_sudo,
                                                        page_or_question),
            })
            return data
        # print("answer_sudo", answer_sudo.search_read())

        # STATE CHANGES TO DONE IN HERE !!!!! CHECK WHY ???

        if answer_sudo.state == 'in_progress':
            if answer_sudo.is_session_answer:
                next_page_or_question = survey_sudo.session_question_id
            else:
                next_page_or_question = survey_sudo._get_next_page_or_question(
                    answer_sudo,
                    answer_sudo.last_displayed_page_id.id if answer_sudo.last_displayed_page_id else 0)

                if next_page_or_question:
                    data.update({
                        'survey_last': survey_sudo._is_last_page_or_question(
                            answer_sudo, next_page_or_question)
                    })
                else:
                    # next_page_or_question=request.env['survey.question'].sudo().search([('id','=',survey_sudo.id)])[0]
                    next_page_or_question = survey_sudo.question_and_page_ids[0]

            if answer_sudo.is_session_answer and next_page_or_question.is_time_limited:
                data.update({
                    'timer_start': survey_sudo.session_question_start_time.isoformat(),
                    'time_limit_minutes': next_page_or_question.time_limit / 60
                })

            data.update({
                page_or_question_key: next_page_or_question,
                'has_answered': answer_sudo.user_input_line_ids.filtered(
                    lambda line: line.question_id == next_page_or_question),
                'can_go_back': survey_sudo._can_go_back(answer_sudo,
                                                        next_page_or_question),
            })
            if survey_sudo.questions_layout != 'one_page':
                data.update({
                    'previous_page_id': survey_sudo._get_next_page_or_question(
                        answer_sudo, next_page_or_question.id, go_back=True).id
                })
        elif answer_sudo.state == 'done' or answer_sudo.survey_time_limit_reached:
            # Display success message
            return self._prepare_survey_finished_values(survey_sudo,
                                                        answer_sudo)

        return data

    @http.route('/survey/<string:survey_token>/<string:answer_token>',
                type='http', auth='public', website=True)
    def survey_display_page(self, survey_token, answer_token, **post):
        access_data = self._get_access_data(survey_token, answer_token,
                                            ensure_token=True)

        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data,
                                             access_data['validity_code'])

        answer_sudo = access_data['answer_sudo']

        answer_sudo.sudo().write({'state': 'in_progress'})
        print("self", )
        return request.render('survey.survey_page_fill',
                              self._prepare_survey_data(
                                  access_data['survey_sudo'], answer_sudo,
                                  **post))

    # Check if question used in calculated metrics
    # @http.route('/survey/used_in_computation', type='json', auth='public', website=True)
    # def survey_used_in_computation(self, **kwargs):
    #     flag = False
    #     question_id = request.env['survey.question'].browse([int(kwargs.get('question_id'))])
    #     survey_id = question_id.survey_id
    #     for question in survey_id.question_ids:
    #         if question.question_type == 'calculated_metric':
    #             if question.calculated_metric_operand1 == question_id.id or question.calculated_metric_operand2 == question_id.id:
    #                 flag = True
    #                 break
    #     return flag

    # def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
    #     """ This method prepares all the data needed for template rendering, in function of the survey user input state.
    #         :param post:
    #             - previous_page_id : come from the breadcrumb or the back button and force the next questions to load
    #                                  to be the previous ones. """
    #     data = {
    #         'is_html_empty': is_html_empty,
    #         'survey': survey_sudo,
    #         'answer': answer_sudo,
    #         'breadcrumb_pages': [{
    #             'id': page.id,
    #             'title': page.title,
    #         } for page in survey_sudo.page_ids],
    #         'format_datetime': lambda dt: format_datetime(request.env, dt, dt_format=False),
    #         'format_date': lambda date: format_date(request.env, date)
    #     }
    #     if survey_sudo.questions_layout != 'page_per_question':
    #         triggering_answer_by_question, triggered_questions_by_answer, selected_answers = answer_sudo._get_conditional_values()
    #         data.update({
    #             'triggering_answer_by_question': {
    #                 question.id: triggering_answer_by_question[question].id for question in triggering_answer_by_question.keys()
    #                 if triggering_answer_by_question[question]
    #             },
    #             'triggered_questions_by_answer': {
    #                 answer.id: triggered_questions_by_answer[answer].ids
    #                 for answer in triggered_questions_by_answer.keys()
    #             },
    #             'selected_answers': selected_answers.ids
    #         })
    #
    #     if not answer_sudo.is_session_answer and survey_sudo.is_time_limited and answer_sudo.start_datetime:
    #         data.update({
    #             'timer_start': answer_sudo.start_datetime.isoformat(),
    #             'time_limit_minutes': survey_sudo.time_limit
    #         })
    #
    #     page_or_question_key = 'question' if survey_sudo.questions_layout == 'page_per_question' else 'page'
    #
    #     # Bypass all if page_id is specified (comes from breadcrumb or previous button)
    #     if 'previous_page_id' in post:
    #         previous_page_or_question_id = int(post['previous_page_id'])
    #         new_previous_id = survey_sudo._get_next_page_or_question(answer_sudo, previous_page_or_question_id, go_back=True).id
    #         page_or_question = request.env['survey.question'].sudo().browse(previous_page_or_question_id)
    #         data.update({
    #             page_or_question_key: page_or_question,
    #             'previous_page_id': new_previous_id,
    #             'has_answered': answer_sudo.user_input_line_ids.filtered(lambda line: line.question_id.id == new_previous_id),
    #             'can_go_back': survey_sudo._can_go_back(answer_sudo, page_or_question),
    #         })
    #         return data
    #
    #     print(">>>>>>>>>>>>>>>>>datadatadatadatadatadata", data, post)
    #     if answer_sudo.state == 'in_progress':
    #         if answer_sudo.is_session_answer:
    #             next_page_or_question = survey_sudo.session_question_id
    #         else:
    #             next_page_or_question = survey_sudo._get_next_page_or_question(
    #                 answer_sudo,
    #                 answer_sudo.last_displayed_page_id.id if answer_sudo.last_displayed_page_id else 0)
    #
    #             if next_page_or_question:
    #                 data.update({
    #                     'survey_last': survey_sudo._is_last_page_or_question(answer_sudo, next_page_or_question)
    #                 })
    #
    #         if answer_sudo.is_session_answer and next_page_or_question.is_time_limited:
    #             data.update({
    #                 'timer_start': survey_sudo.session_question_start_time.isoformat(),
    #                 'time_limit_minutes': next_page_or_question.time_limit / 60
    #             })
    #
    #         data.update({
    #             page_or_question_key: next_page_or_question,
    #             'has_answered': answer_sudo.user_input_line_ids.filtered(lambda line: line.question_id == next_page_or_question),
    #             'can_go_back': survey_sudo._can_go_back(answer_sudo, next_page_or_question),
    #         })
    #         if survey_sudo.questions_layout != 'one_page':
    #             data.update({
    #                 'previous_page_id': survey_sudo._get_next_page_or_question(answer_sudo, next_page_or_question.id, go_back=True).id
    #             })
    #
    #     elif 'edit' not in post and (answer_sudo.state == 'done' or answer_sudo.survey_time_limit_reached):
    #         # Display success message
    #         return self._prepare_survey_finished_values(survey_sudo, answer_sudo)
    #
    #     elif 'edit' in post:
    #         if answer_sudo.is_session_answer:
    #             next_page_or_question = survey_sudo.session_question_id
    #         else:
    #             next_page_or_question = survey_sudo._get_next_page_or_question(
    #                 answer_sudo,
    #                 answer_sudo.last_displayed_page_id.id if answer_sudo.last_displayed_page_id else 0)
    #
    #         if not next_page_or_question:
    #             next_page_or_question = request.env['survey.question'].browse(survey_sudo.question_and_page_ids.ids[0])
    #
    #         if next_page_or_question:
    #             print("next_page_or_questionnext_page_or_questionnext_page_or_question", answer_sudo,next_page_or_question,survey_sudo)
    #             data.update({
    #                 'survey_last': True
    #             })
    #         print("next_page_or_questionnext_page_or_questionnext_page_or_question",next_page_or_question)
    #         if answer_sudo.is_session_answer and next_page_or_question.is_time_limited:
    #             data.update({
    #                 'timer_start': survey_sudo.session_question_start_time.isoformat(),
    #                 'time_limit_minutes': next_page_or_question.time_limit / 60
    #             })
    #
    #         data.update({
    #             page_or_question_key: next_page_or_question,
    #             'has_answered': answer_sudo.user_input_line_ids.filtered(lambda line: line.question_id == next_page_or_question),
    #             'can_go_back': survey_sudo._can_go_back(answer_sudo, next_page_or_question),
    #         })
    #         if survey_sudo.questions_layout != 'one_page':
    #             data.update({
    #                 'previous_page_id': survey_sudo._get_next_page_or_question(answer_sudo, next_page_or_question.id, go_back=True).id
    #             })
    #
    #     print(">>>>>>>>>>>>>>>>>datadatadatadatadatadata",data,post)
    #     # 5 / 0
    #     return data

    @http.route('/survey/used_in_computation', type='json', auth='public',
                website=True)
    def survey_used_in_computation(self, **kwargs):
        flag = False
        question_id = request.env['survey.question'].browse(
            [int(kwargs.get('question_id'))])
        # survey_id = question_id.survey_id
        # for question in survey_id.question_ids:
        #     if question.question_type == 'calculated_metric':
        #         if question.calculated_metric_operand1 == question_id.id or question.calculated_metric_operand2 == question_id.id:
        #             flag = True
        #             break
        return [{'id': question_id.calculated_metric_operand1.id,
                 'type': question_id.calculated_metric_operand1.question_type},
                {'id': question_id.calculated_metric_operand2.id,
                 'type': question_id.calculated_metric_operand2.question_type}]

    @http.route('/survey/get_calculated_metric_info_answer', type='json',
                auth='public', website=True)
    def survey_calculated_metric_info_answer(self, **kwargs):
        calculated_metrics = request.env['survey.question'].sudo().search(['|',
                                                                           (
                                                                           'calculated_metric_operand1',
                                                                           '=',
                                                                           int(kwargs.get(
                                                                               'question_id'))),
                                                                           (
                                                                           'calculated_metric_operand2',
                                                                           '=',
                                                                           int(kwargs.get(
                                                                               'question_id')))])
        for calculated_metric in calculated_metrics:
            dict_add = True
            dict = {}
            for lst in kwargs.get('answer_lst'):
                if int(lst['question_id']) == calculated_metric.id:
                    lst[kwargs.get('question_id')] = kwargs.get('answer')
                    dict = lst
                    dict_add = False
                    break;

            if dict_add:
                if calculated_metric.calculated_metric_operand1.id == int(
                        kwargs.get('question_id')):
                    dict[
                        str(calculated_metric.calculated_metric_operand1.id)] = kwargs.get(
                        'answer')
                else:
                    dict[
                        str(calculated_metric.calculated_metric_operand1.id)] = ''
                if calculated_metric.calculated_metric_operand2.id == int(
                        kwargs.get('question_id')):
                    dict[
                        str(calculated_metric.calculated_metric_operand2.id)] = kwargs.get(
                        'answer')
                else:
                    dict[
                        str(calculated_metric.calculated_metric_operand2.id)] = ''

                dict['question_id'] = str(calculated_metric.id)
            result = self.survey_calculated_metric_info2(dict)
            dict['answer'] = result
            add = True
            for lst in kwargs.get('answer_lst'):
                if lst['question_id'] == dict['question_id']:
                    lst['answer'] = dict['answer']
                    add = False
                    break;
            if add:
                kwargs.get('answer_lst').append(dict)
        return kwargs.get('answer_lst')

    def survey_calculated_metric_info2(self, kwargs):
        # 5/0
        answer = 0
        question_id = request.env['survey.question'].browse(
            [int(kwargs.get('question_id'))])
        operand1_question = question_id.calculated_metric_operand1
        operand2_question = question_id.calculated_metric_operand2
        operator = question_id.calculated_operator

        # Operand 1
        if operand1_question.question_type == 'numerical_box' or operand1_question.question_type == 'progress_bar' and \
                (
                        operand2_question.question_type == 'numerical_box' or operand2_question.question_type == 'progress_bar' \
                        or operand2_question.question_type == 'date' or operand2_question.question_type == 'datetime'):
            if kwargs.get(str(operand1_question.id)) != '':
                operand1_value = int(kwargs.get(str(operand1_question.id)))
            else:
                operand1_value = ''
        elif operand1_question.question_type == 'date':
            if kwargs.get(str(operand1_question.id)) != '':
                operand1_value = datetime.strptime(
                    kwargs.get(str(operand1_question.id)), "%m/%d/%Y")
            else:
                operand1_value = ''
        elif operand1_question.question_type == 'datetime':
            if kwargs.get(str(operand1_question.id)) != '':
                operand1_value = datetime.strptime(
                    kwargs.get(str(operand1_question.id)), "%m/%d/%Y %H:%M:%S")
            else:
                operand1_value = ''
        else:
            if kwargs.get(str(operand1_question.id)) != '':
                operand1_value = kwargs.get(str(operand1_question.id))
            else:
                operand1_value = ''

        # Operand 2
        if operand2_question.question_type == 'numerical_box' or operand2_question.question_type == 'progress_bar' and \
                (
                        operand1_question.question_type == 'numerical_box' or operand1_question.question_type == 'progress_bar' \
                        or operand1_question.question_type == 'date' or operand1_question.question_type == 'datetime'):
            if kwargs.get(str(operand2_question.id)) != '':
                operand2_value = int(kwargs.get(str(operand2_question.id)))
            else:
                operand2_value = ''
        elif operand2_question.question_type == 'date':
            if kwargs.get(str(operand2_question.id)) != '':
                operand2_value = datetime.strptime(
                    kwargs.get(str(operand2_question.id)), "%m/%d/%Y")
            else:
                operand2_value = ''
        elif operand2_question.question_type == 'datetime':
            if kwargs.get(str(operand2_question.id)) != '':
                operand2_value = datetime.strptime(
                    kwargs.get(str(operand2_question.id)), "%m/%d/%Y %H:%M:%S")
            else:
                operand2_value = ''
        else:
            if kwargs.get(str(operand2_question.id)) != '':
                operand2_value = kwargs.get(str(operand2_question.id))
            else:
                operand2_value = ''

        # Computation
        if operator.type == 'add':
            if operand1_question.question_type == 'date' or operand1_question.question_type == 'datetime':
                # if operand2_question.question_type == 'date' or operand2_question.question_type == 'datetime':
                #     print('>>>>>>>>',operand1_value,operand2_value)
                #     if operand2_value != '' and operand1_value != '':
                #         answer = operand1_value + operand2_value
                #     elif operand2_value != '':
                #         answer = operand2_value
                #     else:
                #         answer = operand1_value
                if operand2_question.question_type != 'char_box' and operand2_question.question_type != 'text_box':
                    if operand2_value != '' and operand1_value != '':
                        answer = operand1_value + timedelta(days=operand2_value)
                    elif operand2_value != '':
                        answer = operand2_value
                    else:
                        answer = operand1_value
                else:
                    if operand1_question.question_type == 'datetime':
                        if operand2_value != '' and operand1_value != '':
                            answer = operand1_value.strftime(
                                "%Y-%m-%d %H:%M:%S") + " " + operand2_value
                        elif operand1_value != '':
                            answer = operand1_value.strftime(
                                "%Y-%m-%d %H:%M:%S")
                        else:
                            answer = operand2_value
                    else:
                        if operand2_value != '' and operand1_value != '':
                            answer = operand1_value.strftime(
                                "%Y-%m-%d") + " " + operand2_value
                        elif operand1_value != '':
                            answer = operand1_value.strftime("%Y-%m-%d")
                        else:
                            answer = operand2_value
            elif operand2_question.question_type == 'date' or operand2_question.question_type == 'datetime':
                if operand1_question.question_type != 'char_box' and operand1_question.question_type != 'text_box':
                    if operand2_value != '' and operand1_value != '':
                        answer = operand2_value + timedelta(days=operand1_value)
                    elif operand2_value != '':
                        answer = operand2_value
                    else:
                        answer = operand1_value
                else:
                    if operand2_question.question_type == 'datetime':
                        if operand2_value != '' and operand1_value != '':
                            answer = operand1_value + " " + operand2_value.strftime(
                                "%Y-%m-%d %H:%M:%S")
                        elif operand2_value != '':
                            answer = operand2_value.strftime(
                                "%Y-%m-%d %H:%M:%S")
                        else:
                            answer = operand1_value
                    else:
                        if operand2_value != '' and operand1_value != '':
                            answer = operand1_value + " " + operand2_value.strftime(
                                "%Y-%m-%d")
                        elif operand2_value != '':
                            answer = operand2_value.strftime("%Y-%m-%d")
                        else:
                            answer = operand1_value
            else:
                if operand2_question.question_type == 'char_box' or operand2_question.question_type == 'text_box':
                    answer = str(operand1_value) + " " + operand2_value
                elif operand1_question.question_type == 'char_box' or operand1_question.question_type == 'text_box':
                    answer = operand1_value + " " + str(operand2_value)
                elif operand1_value != '' and operand2_value != '':
                    answer = operand1_value + operand2_value
                elif operand1_value != '':
                    answer = operand1_value
                else:
                    answer = operand2_value
        elif operator.type == 'subtract':
            if operand1_question.question_type == 'date' or operand1_question.question_type == 'datetime':
                if operand2_question.question_type == 'date' or operand2_question.question_type == 'datetime':
                    if operand2_value != '' and operand1_value != '':
                        answer = operand1_value - operand2_value
                    elif operand2_value != '':
                        answer = operand2_value
                    else:
                        answer = operand1_value
                else:
                    if operand2_value != '' and operand1_value != '':
                        answer = operand1_value - timedelta(days=operand2_value)
                    elif operand2_value != '':
                        answer = operand2_value
                    else:
                        answer = operand1_value
                # answer = operand1_value - timedelta(days=operand2_value)
            elif operand2_question.question_type == 'date' or operand2_question.question_type == 'datetime':
                # answer = operand2_value - timedelta(days=operand1_value)
                if operand2_value != '' and operand1_value != '':
                    answer = operand2_value - timedelta(days=operand1_value)
                elif operand2_value != '':
                    answer = operand2_value
                else:
                    answer = operand1_value
            else:
                if operand1_value != '' and operand2_value != '':
                    answer = operand1_value - operand2_value
                elif operand1_value != '':
                    answer = operand1_value
                else:
                    answer = -operand2_value

        elif operator.type == 'multiply':
            if operand1_value != '' and operand2_value != '':
                answer = operand1_value * operand2_value
        elif operator.type == 'divide':
            if operand1_value != '' and operand2_value != '':
                if operand2_value > 0:
                    answer = operand1_value / operand2_value
        return str(answer)

    # Compute the answer for calculated metric question type
    @http.route('/survey/get_calculated_metric_info', type='http',
                auth='public', website=True)
    def survey_calculated_metric_info(self, **kwargs):
        answer = 0
        question_id = request.env['survey.question'].browse(
            [int(kwargs.get('question_id'))])
        operand1_question = question_id.calculated_metric_operand1
        operand2_question = question_id.calculated_metric_operand2
        operator = question_id.calculated_operator

        # Operand 1
        if operand1_question.question_type == 'numerical_box' or operand1_question.question_type == 'progress_bar' and \
                (
                        operand2_question.question_type == 'numerical_box' or operand2_question.question_type == 'progress_bar' \
                        or operand2_question.question_type == 'date' or operand2_question.question_type == 'datetime'):
            operand1_value = int(kwargs.get(str(operand1_question.id)))
        elif operand1_question.question_type == 'date':
            operand1_value = datetime.strptime(
                kwargs.get(str(operand1_question.id)), "%Y-%m-%d")
        elif operand1_question.question_type == 'datetime':
            operand1_value = datetime.strptime(
                kwargs.get(str(operand1_question.id)), "%Y-%m-%d %H:%M:%S")
        else:
            operand1_value = kwargs.get(str(operand1_question.id))

        # Operand 2
        if operand2_question.question_type == 'numerical_box' or operand2_question.question_type == 'progress_bar' and \
                (
                        operand1_question.question_type == 'numerical_box' or operand1_question.question_type == 'progress_bar' \
                        or operand1_question.question_type == 'date' or operand1_question.question_type == 'datetime'):
            operand2_value = int(kwargs.get(str(operand2_question.id)))
        elif operand2_question.question_type == 'date':
            operand2_value = datetime.strptime(
                kwargs.get(str(operand2_question.id)), "%Y-%m-%d")
        elif operand2_question.question_type == 'datetime':
            operand2_value = datetime.strptime(
                kwargs.get(str(operand2_question.id)), "%Y-%m-%d %H:%M:%S")
        else:
            operand2_value = kwargs.get(str(operand2_question.id))

        # Computation
        if operator.type == 'add':
            if operand1_question.question_type == 'date' or operand1_question.question_type == 'datetime':
                if operand2_question.question_type != 'char_box' and operand2_question.question_type != 'text_box':
                    answer = operand1_value + timedelta(days=operand2_value)
                else:
                    answer = operand1_value.strftime(
                        "%Y-%m-%d %H:%M:%S") + " " + operand2_value
            elif operand2_question.question_type == 'date' or operand2_question.question_type == 'datetime':
                if operand1_question.question_type != 'char_box' and operand1_question.question_type != 'text_box':
                    answer = operand2_value + timedelta(days=operand1_value)
                else:
                    answer = operand1_value + " " + operand2_value.strftime(
                        "%Y-%m-%d %H:%M:%S")
            else:
                if operand2_question.question_type == 'char_box' or operand2_question.question_type == 'text_box':
                    answer = operand1_value + " " + operand2_value
                else:
                    answer = operand1_value + operand2_value
        elif operator.type == 'subtract':
            if operand1_question.question_type == 'date' or operand1_question.question_type == 'datetime':
                answer = operand1_value - timedelta(days=operand2_value)
            elif operand2_question.question_type == 'date' or operand2_question.question_type == 'datetime':
                answer = operand2_value - timedelta(days=operand1_value)
            else:
                answer = operand1_value - operand2_value
        elif operator.type == 'multiply':
            answer = operand1_value * operand2_value
        elif operator.type == 'divide':
            if operand2_value > 0:
                answer = operand1_value / operand2_value
        return str(answer)

    # @http.route(
    #     '/survey/next_question/<string:survey_token>/<string:answer_token>',
    #     type='json', auth='public', website=True)
    # def survey_next_question(self, survey_token, answer_token, **post):
    #     """ Method used to display the next survey question in an ongoing session.
    #     Triggered on all attendees screens when the host goes to the next question. """
    #     print("HHHHHHAHAHAHHAHAHAHAHAHAHHAHAHAHAHHFYTFV")
    #     access_data = self._get_access_data(survey_token, answer_token,
    #                                         ensure_token=True)
    #     if access_data['validity_code'] is not True:
    #         return {'error': access_data['validity_code']}
    #     survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
    #         'answer_sudo']
    #
    #     if answer_sudo.state == 'new' and answer_sudo.is_session_answer:
    #         answer_sudo._mark_in_progress()
    #
    #     return self._prepare_question_html(survey_sudo, answer_sudo, **post)

    def _prepare_question_html(self, survey_sudo, answer_sudo, **post):
        """ Survey page navigation is done in AJAX. This function prepare the 'next page' to display in html
        and send back this html to the survey_form widget that will inject it into the page."""
        print("survey_sudo", survey_sudo)
        print("answer_sudo", answer_sudo)
        survey_data = self._prepare_survey_data(survey_sudo, answer_sudo,
                                                **post)
        # print("survey data", survey_data)
        # answer_sudo.state = 'in_progress'
        survey_content = False
        if answer_sudo.state == 'done':
            print('if', answer_sudo.state)
            survey_content = request.env.ref(
                'survey.survey_fill_form_done')._render(survey_data)
        else:
            # print('else', answer_sudo.state)
            survey_content = request.env.ref(
                'survey.survey_fill_form_in_progress')._render(survey_data)
            # print('survey_content', survey_content)

        survey_progress = False
        if answer_sudo.state == 'in_progress' and not survey_data.get(
                'question', request.env['survey.question']).is_page:
            if survey_sudo.questions_layout == 'page_per_section':
                page_ids = survey_sudo.page_ids.ids
                survey_progress = request.env.ref(
                    'survey.survey_progression')._render({
                    'survey': survey_sudo,
                    'page_ids': page_ids,
                    'page_number': page_ids.index(survey_data['page'].id) + (
                        1 if survey_sudo.progression_mode == 'number' else 0)
                })
            elif survey_sudo.questions_layout == 'page_per_question':
                page_ids = survey_sudo.question_ids.ids
                survey_progress = request.env.ref(
                    'survey.survey_progression')._render({
                    'survey': survey_sudo,
                    'page_ids': page_ids,
                    'page_number': page_ids.index(survey_data['question'].id)
                })

        return {
            'survey_content': survey_content,
            'survey_progress': survey_progress,
            'survey_navigation': request.env.ref(
            'survey.survey_navigation')._render(survey_data),
        }

    @http.route('/survey/submit/<string:survey_token>/<string:answer_token>',
                type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):

        """ Submit a page from the survey.
        This will take into account the validation errors and store the answers to the questions.
        If the time limit is reached, errors will be skipped, answers will be ignored and
        survey state will be forced to 'done'"""

        survey = request.env['survey.survey'].search([
            ('access_token', '=', survey_token)])
        if survey.questions_layout == 'page_per_question':
            question = request.env['survey.question'].browse(int(post['question_id']))
            if question.question_type == 'toggle':
                answer = None
                question_id = int(question.id)
                if post[str(question_id)] == True:
                    answer = 'Yes'
                elif post[str(question_id)] == False:
                    answer = 'No'
                answer_ques = request.env['survey.question.answer'].search([
                    ('question_id', '=', question_id),
                    ('value', '=', answer)])
                post[str(question_id)] = str(answer_ques.id)

        access_data = self._get_access_data(survey_token, answer_token,
                                            ensure_token=True)

        if access_data['validity_code'] is not True:
            return {'error': access_data['validity_code']}
        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data[
            'answer_sudo']
        print('answer_sudo', answer_sudo)
        print('survey_sudo', survey_sudo)

        # STATE IN PROGRESSS

        if answer_sudo.state == 'done':
            return {'error': 'unauthorized'}

        questions, page_or_question_id = survey_sudo._get_survey_questions(
            answer=answer_sudo,
            page_id=post.get('page_id'),
            question_id=post.get('question_id'))

        if not answer_sudo.test_entry and not survey_sudo._has_attempts_left(
                answer_sudo.partner_id, answer_sudo.email,
                answer_sudo.invite_token):
            # prevent cheating with users creating multiple 'user_input' before their last attempt
            return {'error': 'unauthorized'}

        if answer_sudo.survey_time_limit_reached or answer_sudo.question_time_limit_reached:
            if answer_sudo.question_time_limit_reached:
                time_limit = survey_sudo.session_question_start_time + relativedelta(
                    seconds=survey_sudo.session_question_id.time_limit
                )
                time_limit += timedelta(seconds=3)
            else:
                time_limit = answer_sudo.start_datetime + timedelta(
                    minutes=survey_sudo.time_limit)
                time_limit += timedelta(seconds=10)
            if fields.Datetime.now() > time_limit:
                # prevent cheating with users blocking the JS timer and taking all their time to answer
                return {'error': 'unauthorized'}

        errors = {}
        selected_answer = []
        # Prepare answers / comment by question, validate and save answers
        print("QUESTIONS----> ", questions)
        for question in questions:
            print('QUESTION----> ', question)

            if question.question_type == 'toggle':
                selected_answer.append(answer_sudo.id)

            inactive_questions = request.env[
                'survey.question'] if answer_sudo.is_session_answer else answer_sudo._get_inactive_conditional_questions()
            print('INACTIVE QUESTIONS----->', inactive_questions)
            if question in inactive_questions:  # if question is inactive, skip validation and save
                answer, comment = self._extract_comment_from_answers(question,
                                                                     post.get(
                                                                         str(question.id)))
                # print('QUESTION---->', question)
                # print('ANSWER----> ', answer)
                # print('COMMENT----> ', comment)
                answer_sudo.save_lines(question, answer, comment)
                # continue
            answer, comment = self._extract_comment_from_answers(question,
                                                                 post.get(
                                                                     str(question.id)))
            # print('ANSWER___', answer)
            # if question.question_type == 'toggle':
            #     answer = post.get(str(question.id))
            errors.update(question.validate_question(answer, comment))
            if not errors.get(question.id):
                # print('looped')
                # print('_____anser', answer_sudo.save_lines(question, answer, comment))
                answer_sudo.save_lines(question, answer, comment)
            # print('errors....', errors)

        if errors and not (
                answer_sudo.survey_time_limit_reached or answer_sudo.question_time_limit_reached):
            return {'error': 'validation', 'fields': errors}

        if not answer_sudo.is_session_answer:
            answer_sudo._clear_inactive_conditional_answers()

        if answer_sudo.survey_time_limit_reached or survey_sudo.questions_layout == 'one_page':
            answer_sudo._mark_done()
        elif 'previous_page_id' in post:
            # Go back to specific page using the breadcrumb. Lines are saved and survey continues
            return self._prepare_question_html(survey_sudo, answer_sudo, **post)
        else:
            # print("hhehhehehe")
            vals = {'last_displayed_page_id': page_or_question_id}
            if not answer_sudo.is_session_answer:
                next_page = survey_sudo._get_next_page_or_question(answer_sudo,
                                                                   page_or_question_id)
                if not next_page:
                    answer_sudo._mark_done()
            answer_sudo.write(vals)
        # print("____check", self._prepare_question_html(survey_sudo, answer_sudo))
        return self._prepare_question_html(survey_sudo, answer_sudo)
