from odoo import models, fields, api
from odoo.tools.translate import _
from logging import getLogger
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from datetime import datetime


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'
    _description = 'Survey User Input Line for extra fields'

    value_body_map = fields.One2many(
        comodel_name="survey.body.map.value",
        inverse_name="user_input_line_id",
        string="Body Map Value",
        required=False, )

    answer_type = fields.Selection(selection_add=[
        ('body_map', 'Body Map'), ('toggle', 'Toggle'), ('progress_bar', 'Progress Bar'),
        ('calculated_metric', 'Calculated Metric'), ('file', 'File')
    ])
    value_toggle = fields.Boolean('Toggle Answer')
    value_progress_bar = fields.Integer('Progress Bar')
    value_calculated_metric = fields.Char('Calculated Metric')
    value_file = fields.Binary('File', attachment=True)
    file_name = fields.Char('File Name')
    toggle_answer = fields.Char('Toggle Value', store=True, default='')

    @api.constrains('skipped', 'answer_type')
    def _check_answer_type_skipped(self):
        for line in self:
            if (line.skipped == bool(line.answer_type)):
                raise ValidationError(_('A question can either be skipped or answered, not both.'))

            # allow 0 for numerical box
            if line.answer_type == 'toggle':
                continue
            if line.answer_type == 'numerical_box' and float_is_zero(line['value_numerical_box'], precision_digits=6):
                continue
            if line.answer_type == 'suggestion':
                field_name = 'suggested_answer_id'
            elif line.answer_type:
                field_name = 'value_%s' % line.answer_type
            else:  # skipped
                field_name = False
            if field_name != 'value_progress_bar':
                if field_name and not line[field_name]:
                    raise ValidationError(_('The answer must be in the right type'))

    def get_survey_user_input_line_data(self, survey, user, start_date, end_date):
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        survey_data = []
        if survey:
            if survey != "none":
                if user == "none":
                    survey_data = self.env['survey.user_input'].search(
                        [('survey_id', '=', int(survey)), ('create_date', '>=', start_date),
                         ('create_date', '<=', end_date)])
                else:
                    survey_data = self.env['survey.user_input'].search(
                        [('survey_id', '=', int(survey)), ('create_date', '>=', start_date),
                         ('create_date', '<=', end_date),
                         ('create_uid', '=', int(user))])
        header_list = []
        answer_lst = []
        if survey_data:
            header_list.append('Date')
            header_list.append('User')
        for data in survey_data:
            answer = []

            answer.append(data.create_date.strftime("%d/%m/%Y %H:%M:%S"))
            answer.append(data.create_uid.name)
            for que in data.survey_id.question_and_page_ids.filtered(lambda x: not x.is_page):
                res = {}
                res.setdefault('answer', [])
                for line in data.user_input_line_ids:
                    if que.title not in header_list:
                        header_list.append(que.title)

                    if line.question_id.id == que.id:
                        if line.suggested_answer_id:
                            if line.matrix_row_id:
                                res['answer'].append(line.matrix_row_id.value + ": " + line.suggested_answer_id.value)
                            else:
                                res['answer'].append(line.suggested_answer_id.value)
                        elif line.value_char_box:
                            res['answer'].append(line.value_char_box)
                        elif line.value_numerical_box:
                            res['answer'].append(line.value_numerical_box)
                        elif line.value_date:
                            res['answer'].append(line.value_date.strftime("%d/%m/%Y"))
                        elif line.value_datetime:
                            res['answer'].append(line.value_datetime.strftime("%d/%m/%Y %H:%M:%S"))
                        elif line.value_text_box:
                            res['answer'].append(line.value_text_box)
                        elif que.question_type == 'toggle':
                            if que.toggle_on_name and que.toggle_off_name:
                                if line.value_toggle == True:
                                    res['answer'].append(que.toggle_on_name)
                                else:
                                    res['answer'].append(que.toggle_off_name)
                            else:
                                if line.value_toggle == True:
                                    res['answer'].append('True')
                                else:
                                    res['answer'].append('False')
                        elif line.value_progress_bar:
                            res['answer'].append(line.value_progress_bar)
                        elif line.value_calculated_metric:
                            res['answer'] = []

                            res['answer'].append(line.value_calculated_metric)
                        elif line.value_body_map:
                            list_string = []
                            for value in line.value_body_map:
                                line_string = ''
                                if value.pain_level:
                                    line_string = 'Pain Level[' + str(value.pain_level) + ']'
                                if value.comment:
                                    line_string += ' (' + value.comment + ')'
                                list_string.append(line_string)
                            res['answer'] = list_string
                        elif line.value_file:
                            res['answer'].append(
                                {'question_id': que.id, 'answer_id': data.id, 'access_token': data.access_token})

                answer.append(res.get('answer'))
            answer_lst.append(answer)
        # print(">>>>>>>>>header_list", header_list, answer_lst)
        return {'header_list': header_list, 'answer_lst': answer_lst}
