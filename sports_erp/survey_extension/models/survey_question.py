# # -*- coding: utf-8 -*-
# ###############################################################################
# #    License, author and contributors information in:                         #
# #    __manifest__.py file at the root folder of this module.                  #
# ###############################################################################
#
# from odoo import models, fields, api
# from odoo.tools.translate import _
# from logging import getLogger
#
#
# class SurveyQuestion(models.Model):
#     _inherit = 'survey.question'
#
#     question_type = fields.Selection(selection_add=[
#         ('body_map', 'Body Map'), ('toggle', 'Toggle'),
#         ('progress_bar', 'Progress Bar'),
#         ('calculated_metric', 'Calculated Metric'), ('file', 'File')
#     ])
#     min_width = fields.Integer('Start')
#     max_width = fields.Integer('End')
#     step = fields.Integer('Step')
#     toggle_on_name = fields.Char('Toggle On Name')
#     toggle_off_name = fields.Char('Toggle Off Name')
#     calculated_metric_operand1 = fields.Many2one('survey.question',
#                                                  'Metric Operand 1')
#     calculated_metric_operand2 = fields.Many2one('survey.question',
#                                                  'Metric Operand 2')
#     calculated_operator = fields.Many2one('calculated.metric.operator',
#                                           'Operator')
#     in_portal_show = fields.Boolean('In Portal Show')
#     set_color = fields.Selection(
#         [('red_to_green', 'Red To Green'), ('green_to_red', 'Green To Red')],
#         string="Set Color", default="red_to_green")
#     triggering_question_id = fields.Many2one(
#         'survey.question', string="Triggering Question", copy=False,
#         compute="_compute_triggering_question_id",
#         store=True, readonly=False,
#         help="Question containing the triggering answer to display the current question.",
#         domain="""[('survey_id', '=', survey_id),
#                      '&', ('question_type', 'in', ['simple_choice', 'multiple_choice','toggle']),
#                      '|',
#                          ('sequence', '<', sequence),
#                          '&', ('sequence', '=', sequence), ('id', '<', id)]""")
#
#     @api.onchange('question_type')
#     def on_change_question_type(self):
#         for rec in self._origin:
#             calculated_metrics = self.env['survey.question'].search(
#                 ['|', ('calculated_metric_operand1', '=', rec.id),
#                  ('calculated_metric_operand2', '=', rec.id)])
#             for calculated_metric in calculated_metrics:
#                 calculated_metric.calculated_operator = False
#             print(">>>>>>>>>>>>>>>>>>>>dddddd>>>>>>")
#         for rec in self:
#             print(">>ffff>>>>>>>>>>>>>>>>>>>>>>22222>>")
#             if rec.question_type == 'toggle':
#                 print(">>>>>>>>>>>>>>>>>>>>>>>>22222>>")
#                 self.env['survey.question.answer'].create(
#                     {'question_id': rec.id, 'value': 'Yes'})
#                 self.env['survey.question.answer'].create(
#                     {'question_id': rec.id, 'value': 'No'})
#             else:
#                 print(">>>>>>>>>>>>>>>444444>>>>>>>>>22222>>")
#                 for res in rec.suggested_answer_ids:
#                     res.unlink()
#
#     @api.onchange('calculated_metric_operand1', 'calculated_metric_operand2')
#     def on_change_calculate_operator(self):
#         list_of_operators = []
#         for rec in self:
#             rec.calculated_operator = False
#             if rec.question_type == 'calculated_metric' and rec.calculated_metric_operand1 and rec.calculated_metric_operand2:
#                 if rec.calculated_metric_operand1.question_type in [
#                     'numerical_box', 'progress_bar'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'numerical_box', 'progress_bar']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search([]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'text_box', 'char_box'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'char_box', 'text_box']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', '=', 'add')]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'numerical_box', 'text_box'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'numerical_box', 'text_box']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', '=', 'add')]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'progress_bar', 'text_box'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'progress_bar', 'text_box']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', '=', 'add')]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'numerical_box', 'char_box'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'numerical_box', 'char_box']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', '=', 'add')]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'progress_bar', 'char_box'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'progress_bar', 'char_box']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', '=', 'add')]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'numerical_box', 'date'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'numerical_box', 'date']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', 'in', ['add', 'subtract'])]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'numerical_box', 'datetime'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'numerical_box', 'datetime']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', 'in', ['add', 'subtract'])]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'progress_bar', 'date'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'progress_bar', 'date']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', 'in', ['add', 'subtract'])]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'progress_bar', 'datetime'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'progress_bar', 'datetime']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', 'in', ['add', 'subtract'])]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'char_box', 'date', 'text_box'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'char_box', 'date', 'text_box']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', '=', 'add')]).ids
#                 elif rec.calculated_metric_operand1.question_type in [
#                     'char_box', 'datetime', 'text_box'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'char_box', 'datetime', 'text_box']:
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', '=', 'add')]).ids
#                 if rec.calculated_metric_operand1.question_type in ['date',
#                                                                     'datetime'] and \
#                         rec.calculated_metric_operand2.question_type in [
#                     'date', 'datetime']:
#                     # list_of_operators = self.env['calculated.metric.operator'].search([('id','in',[])]).ids
#                     list_of_operators = self.env[
#                         'calculated.metric.operator'].search(
#                         [('type', 'in', ['subtract'])]).ids
#                 if list_of_operators:
#                     return {
#                         'domain': {
#                             'calculated_operator': [
#                                 ('id', 'in', list_of_operators)],
#                         }}
#         return {
#             'domain': {
#                 'calculated_operator': [('id', 'in', [])],
#             }}
#
#     @api.model
#     def create(self, values):
#         res = super(SurveyQuestion, self).create(values)
#         if 'question_type' in values:
#             if values.get('question_type') == 'toggle':
#                 self.env['survey.question.answer'].create(
#                     {'question_id': res.id, 'value': 'Yes'})
#                 self.env['survey.question.answer'].create(
#                     {'question_id': res.id, 'value': 'No'})
#         return res
#
#     def write(self, values):
#         recs = super(SurveyQuestion, self).write(values)
#         print(">>>>>>>>>", values, self)
#         if 'question_type' in values:
#             if values.get('question_type') == 'toggle':
#                 self.env['survey.question.answer'].create(
#                     {'question_id': self.id, 'value': 'Yes'})
#                 self.env['survey.question.answer'].create(
#                     {'question_id': self.id, 'value': 'No'})
#         return recs
#
#     # @api.onchange('triggering_answer_id')
#     # def triggering_answer_id(self):
#     #     print('triggering_answer', self.triggering_answer_id)
#
#
#
# # class CalculatedMetricOperator(models.Model):
# #     _name = 'calculated.metric.operator'
# #     _sql_constraints = [
# #         ('type_unique', 'unique (type)',
# #          "A Operator of this type already exists."),
# #     ]
# #
# #     name = fields.Char('Name', required=1)
# #     type = fields.Selection([('add', 'Addition'), ('subtract', 'Subtraction'),
# #                              ('multiply', 'Multiplication'),
# #                              ('divide', 'Division')],
# #                             string='Type', default='add')
