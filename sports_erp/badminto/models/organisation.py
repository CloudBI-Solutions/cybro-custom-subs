from odoo import fields, models


class Organisation(models.Model):
    _inherit = 'organisation.organisation'

    technical_configuration_ids = fields.One2many('technical.configuration',
                                                  'organisation_id')


class TechnicalConfigurationType(models.Model):
    _name = 'technical.configuration.types'

    name = fields.Char()


class TechnicalConfiguration(models.Model):
    _name = 'technical.configuration'

    type = fields.Many2one('technical.configuration.types')
    configuration_ids = fields.One2many(
        'technical.assessment.configuration.data',
        'technical_config_id')
    organisation_id = fields.Many2one('organisation.organisation')
