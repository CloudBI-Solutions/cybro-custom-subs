from odoo import models, fields


class Events(models.Model):
    _inherit = 'event.event'

    event_extension = fields.Boolean('Event Extension')