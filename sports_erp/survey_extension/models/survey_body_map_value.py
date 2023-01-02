from odoo import models, fields, api
from odoo.tools.translate import _
from logging import getLogger


class SurveyUserInputLineAudit(models.Model):
    _name = 'survey.body.map.value'

    pain_level = fields.Integer('Pain Level')
    comment = fields.Text('Comment')
    x_value = fields.Float('X Value')
    y_value = fields.Float('Y Value')
    user_input_line_id = fields.Many2one(
        comodel_name="survey.user_input.line",
        string="User input line",
        required=False,)


    def create_data(self,dict):
        if 'question' in dict and 'answer' in dict:
            if self.env['survey.user_input'].browse(int(dict.get('answer'))).user_input_line_ids.filtered(
                        lambda l: l.answer_type == 'body_map'):
                if self.env['survey.user_input'].browse(int(dict.get('answer'))).user_input_line_ids.filtered(
                    lambda l: l.answer_type == 'body_map').value_body_map.filtered(
                    lambda t: t.x_value == float(dict.get('x_value')) and t.y_value == float(dict.get('y_value'))):
                    self.env['survey.user_input'].browse(int(dict.get('answer'))).user_input_line_ids.filtered(
                        lambda l: l.answer_type == 'body_map').value_body_map.filtered(
                        lambda t: t.x_value == float(dict.get('x_value')) and t.y_value == float(dict.get('y_value'))).write({'comment':dict.get('comment'),'pain_level':int(dict.get('pain_level'))})
                else:
                    self.env['survey.user_input'].browse(int(dict.get('answer'))).user_input_line_ids.filtered(
                        lambda l: l.answer_type == 'body_map').write({'question_id': dict.get('question'),'value_body_map' :[(0, 0, {'pain_level':int(dict.get('pain_level')),'comment':dict.get('comment'),'x_value':float(dict.get('x_value')),'y_value':float(dict.get('y_value'))})]})
            else:
                vals = {
                    'user_input_id': dict.get('answer'),
                    'question_id': dict.get('question'),
                    'skipped': False,
                    'answer_type': 'body_map',
                    'value_body_map': [(0, 0, {'pain_level':int(dict.get('pain_level')),'comment':dict.get('comment'),'x_value':float(dict.get('x_value')),'y_value':float(dict.get('y_value'))})]
                }
                self.env['survey.user_input.line'].create(vals)
        # self.env['survey.user_input.line'].create({''})
        # data = self.sudo().create(dict)
        return True


    def delete_body_map_value(self,dict):
        if dict.get('x_value') != '' and dict.get('y_value') != '':
            self.env['survey.body.map.value'].search([('x_value','=',dict.get('x_value')),('y_value','=',dict.get('y_value'))]).unlink()
            return True
        return False

    def get_body_map_value_data(self,answer_id):
        if answer_id:
            if self.env['survey.user_input'].browse(int(answer_id)).user_input_line_ids.filtered(
                        lambda l: l.answer_type == 'body_map'):
                ids = self.env['survey.user_input'].browse(int(answer_id)).user_input_line_ids.filtered(
                        lambda l: l.answer_type == 'body_map').value_body_map.ids

                body_map_value_data = self.env['survey.body.map.value'].search_read([('id','in',ids)])
                return body_map_value_data
            return []
        return []
