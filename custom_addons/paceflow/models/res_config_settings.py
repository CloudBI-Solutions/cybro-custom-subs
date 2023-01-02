# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mobile = fields.Selection(selection=[('12', 'One'), ('6', 'Two')],
                              string='Mobile Device', default='12')

    tablet = fields.Selection(selection=[('6', 'Two'), ('4', 'Three')],
                              string='Tablet Device', default='6')

    desktop = fields.Selection(selection=[('4', 'Three'), ('3', 'Four')],
                               string='Desktop Device', default='4')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'paceflow.mobile', self.mobile)
        self.env['ir.config_parameter'].set_param(
            'paceflow.tablet', self.tablet)
        self.env['ir.config_parameter'].set_param(
            'paceflow.desktop', self.desktop)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            mobile=params.get_param('paceflow.mobile'),
            tablet=params.get_param('paceflow.tablet'),
            desktop=params.get_param('paceflow.desktop'),
        )
        return res
