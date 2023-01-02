from odoo import models, fields


class Survey(models.Model):
    _inherit = 'survey.survey'

    is_diary = fields.Boolean()