from odoo import models, fields, api


class Organisation(models.Model):
    _inherit = 'organisation.organisation'

    lifestyle_assessment_data_id = fields.Many2one('survey.survey',
                                                   default=lambda self: self.env.ref('organisation_diaries.lifestyle_assessment_survey'), domain="[('is_diary', '=', True)]")
    sc_assessment_data_id = fields.Many2one('survey.survey',
                                            default=lambda self: self.env.ref('organisation_diaries.sc_assessment_survey'), domain="[('is_diary', '=', True)]")
    mobility_assessment_data_id = fields.Many2one('survey.survey',
                                                  default=lambda self: self.env.ref('organisation_diaries.mobility_assessment_survey'), domain="[('is_diary', '=', True)]")
    hrv_assessment_data_id = fields.Many2one('survey.survey',
                                             default=lambda self: self.env.ref('organisation_diaries.hr_assessment_survey'), domain="[('is_diary', '=', True)]")
    nutrition_assessment_data_id = fields.Many2one('survey.survey',
                                                   default=lambda self: self.env.ref('organisation_diaries.nutrition_assessment_survey'), domain="[('is_diary', '=', True)]")
    mental_assessment_data_id = fields.Many2one('survey.survey',
                                                default=lambda self: self.env.ref('organisation_diaries.mental_assessment_survey'), domain="[('is_diary', '=', True)]")
    aerobic_assessment_data_id = fields.Many2one('survey.survey',
                                                 default=lambda self: self.env.ref('organisation_diaries.aerobic_assessment_survey'), domain="[('is_diary', '=', True)]")
    anaerobic_assessment_data_id = fields.Many2one('survey.survey',
                                                   default=lambda self: self.env.ref('organisation_diaries.anaerobic_assessment_survey'), domain="[('is_diary', '=', True)]")

    lifestyle_assessment_configuration_ids = fields.One2many('lifestyle.assessment.configuration', 'organisation_id')
    hrv_assessment_configuration_ids = fields.One2many('hrv.assessment.configuration', 'organisation_id')
    sc_assessment_configuration_ids = fields.One2many('sc.assessment.configuration', 'organisation_id')
    mobility_assessment_configuration_ids = fields.One2many('mobility.assessment.configuration', 'organisation_id')
    nutrition_assessment_configuration_ids = fields.One2many('nutrition.assessment.configuration', 'organisation_id')
    mental_assessment_configuration_ids = fields.One2many('mental.assessment.configuration', 'organisation_id')
    aerobic_assessment_configuration_ids = fields.One2many('aerobic.assessment.configuration', 'organisation_id')
    anaerobic_assessment_configuration_ids = fields.One2many('anaerobic.assessment.configuration', 'organisation_id')

    @api.onchange('lifestyle_assessment_data_id')
    def onchange_lifestyle_assessment_data_id(self):
        lifestyle_config_ids = []
        for question in self.lifestyle_assessment_data_id.question_and_page_ids.filtered(
            lambda x: not x.is_page and x.question_type == 'calculated_metric'):
            values = {
                'question_id': question.id,
            }
            assessment_config_id = self.env['lifestyle.assessment.configuration'].sudo().create(values)
            lifestyle_config_ids.append(assessment_config_id.id)
        self.lifestyle_assessment_configuration_ids = lifestyle_config_ids


class LifestyleAssessmentConfiguration(models.Model):
    _name = 'lifestyle.assessment.configuration'

    question_id = fields.Many2one('survey.question', domain="[('is_page', '!=', True)]")
    organisation_id = fields.Many2one('organisation.organisation')
    metric_id = fields.Many2one('calculated.metric',)
    visualisation_configuration_id = fields.One2many('visualisation.configuration', 'config_id')


class HRVAssessmentConfiguration(models.Model):
    _name = 'hrv.assessment.configuration'

    question_id = fields.Many2one('survey.question')
    metric_id = fields.Many2one('calculated.metric')
    visualisation_configuration_id = fields.One2many('visualisation.configuration', 'hrv_config_id')
    organisation_id = fields.Many2one('organisation.organisation')


class MobilityAssessmentConfiguration(models.Model):
    _name = 'mobility.assessment.configuration'

    question_id = fields.Many2one('survey.question')
    metric_id = fields.Many2one('calculated.metric')
    visualisation_configuration_id = fields.One2many('visualisation.configuration', 'mobility_config_id')
    organisation_id = fields.Many2one('organisation.organisation')


class MentalAssessmentConfiguration(models.Model):
    _name = 'mental.assessment.configuration'

    question_id = fields.Many2one('survey.question')
    metric_id = fields.Many2one('calculated.metric')
    visualisation_configuration_id = fields.One2many(
        'visualisation.configuration', 'mental_config_id')
    organisation_id = fields.Many2one('organisation.organisation')


class NutritionAssessmentConfiguration(models.Model):
    _name = 'nutrition.assessment.configuration'

    question_id = fields.Many2one('survey.question')
    metric_id = fields.Many2one('calculated.metric')
    visualisation_configuration_id = fields.One2many(
        'visualisation.configuration', 'nutrition_config_id')
    organisation_id = fields.Many2one('organisation.organisation')


class AerobicAssessmentConfiguration(models.Model):
    _name = 'aerobic.assessment.configuration'

    question_id = fields.Many2one('survey.question')
    metric_id = fields.Many2one('calculated.metric')
    visualisation_configuration_id = fields.One2many(
        'visualisation.configuration', 'aerobic_config_id')
    organisation_id = fields.Many2one('organisation.organisation')


class AnaerobicAssessmentConfiguration(models.Model):
    _name = 'anaerobic.assessment.configuration'

    question_id = fields.Many2one('survey.question')
    metric_id = fields.Many2one('calculated.metric')
    visualisation_configuration_id = fields.One2many(
        'visualisation.configuration', 'anaerobic_config_id')
    organisation_id = fields.Many2one('organisation.organisation')


class SCAssessmentConfiguration(models.Model):
    _name = 'sc.assessment.configuration'

    question_id = fields.Many2one('survey.question')
    metric_id = fields.Many2one('calculated.metric')
    visualisation_configuration_id = fields.One2many(
        'visualisation.configuration', 'sc_config_id')
    organisation_id = fields.Many2one('organisation.organisation')


class VisualisationConfiguration(models.Model):
    _name = 'visualisation.configuration'
    _rec_name = 'level'

    config_id = fields.Many2one('lifestyle.assessment.configuration')
    hrv_config_id = fields.Many2one('hrv.assessment.configuration')
    mobility_config_id = fields.Many2one('mobility.assessment.configuration')
    sc_config_id = fields.Many2one('sc.assessment.configuration')
    mental_config_id = fields.Many2one('mental.assessment.configuration')
    nutrition_config_id = fields.Many2one('nutrition.assessment.configuration')
    aerobic_config_id = fields.Many2one('aerobic.assessment.configuration')
    anaerobic_config_id = fields.Many2one('anaerobic.assessment.configuration')
    start = fields.Integer()
    end = fields.Integer()
    level = fields.Selection([('low', 'Low'), ('medium', 'Medium'),
                              ('high', 'High')])
    comments = fields.Text()

