from odoo import models, fields


class TechnicalAssessmentConfiguration(models.Model):
    _name = 'technical.assessment.configuration'
    _description = "Badmintoo Technical Assessment Configuration"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'type'

    type = fields.Many2one('technical.configuration.types')
    technical_ids = fields.One2many('technical.assessment.configuration.data',
                                    'technical_id')


class TechnicalAssessmentConfigurationData(models.Model):
    _name = 'technical.assessment.configuration.data'
    _description = "Badmintoo Technical Assessment Configuration Data"
    _rec_name = 'level'

    organisation_id = fields.Many2one('organisation.organisation')
    start = fields.Float()
    end = fields.Float()
    color = fields.Selection([('red', 'Red'), ('yellow', 'Yellow'),
                              ('green', 'Green')])
    level = fields.Selection([('low', 'Low'), ('medium', 'Medium'),
                              ('high', 'High')])
    comments = fields.Text()
    technical_id = fields.Many2one(
        'technical.assessment.configuration')
    technical_config_id = fields.Many2one('technical.configuration')

