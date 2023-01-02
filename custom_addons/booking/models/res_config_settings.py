# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    time_format = fields.Selection([('12_format', "Use 12 Hour Format"),
                                    ('24_format', "Use 24 Hour Format")],
                                   string="Time Format", store=True,
                                   required=True, default='24_format')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'booking.time_format', self.time_format)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            time_format=params.get_param('booking.time_format'),
        )
        return res
