from odoo import models, fields, api
from random import randint
from odoo import SUPERUSER_ID


class BadmintoAssessmentTypes(models.Model):
    _name = 'assessment.types'
    _description = "Assessment Types"
    _rec_name = 'name'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string='Color', default=_get_default_color)

