from odoo import models, fields


class MetricManagement(models.Model):
    _name = 'metric.management'

    name = fields.Char()
    survey_question_id = fields.Many2one('survey.question')
    calculated_metric_id = fields.Many2one('calculated.metric')
