from odoo import models, fields, api
from random import randint
from odoo import SUPERUSER_ID


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    lifestyle_data_survey_id = fields.Many2one('survey.survey', domain="[('is_diary', '=', True)]", config_parameter='config.lifestyle_data_survey_id')
    hrv_data_survey_id = fields.Many2one('survey.survey', domain="[('is_diary', '=', True)]", config_parameter='config.hrv_data_survey_id')
    mobility_data_survey_id = fields.Many2one('survey.survey', domain="[('is_diary', '=', True)]", config_parameter='config.mobility_data_survey_id')
    mental_data_survey_id = fields.Many2one('survey.survey', domain="[('is_diary', '=', True)]", config_parameter='config.mental_data_survey_id')
    nutrition_data_survey_id = fields.Many2one('survey.survey', domain="[('is_diary', '=', True)]", config_parameter='config.nutrition_data_survey_id')
    sc_data_survey_id = fields.Many2one('survey.survey', domain="[('is_diary', '=', True)]", config_parameter='config.sc_data_survey_id')
    aerobic_data_survey_id = fields.Many2one('survey.survey', domain="[('is_diary', '=', True)]", config_parameter='config.aerobic_data_survey_id')
    anaerobic_data_survey_id = fields.Many2one('survey.survey', domain="[('is_diary', '=', True)]", config_parameter='config.anaerobic_data_survey_id')
