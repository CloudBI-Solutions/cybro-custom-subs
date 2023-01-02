# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import models, api, fields

service_type = [
    ('DLV', 'DLV'),
    ('VAL', 'VAL'),
    ('HAL', 'HAL'),
    ('BLT', 'BLT')
]


class SmsaShippingService(models.Model):
    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(
        selection_add=[('smsa', 'SMSA Express')], ondelete={'smsa': 'cascade'})
    smsa_test_passkey = fields.Char(string="SMSA Test Passkey")
    smsa_prod_passkey = fields.Char(string="SMSA Production Passkey")
    smsa_service = fields.Selection(
        selection=service_type, default="DLV", string="SMSA Service")
    is_cod = fields.Boolean(string="Is COD", default=False)
    


class SMSAProductPackaging(models.Model):
    _inherit = "stock.package.type"

    package_carrier_type = fields.Selection(
        selection_add=[('smsa', 'SMSA Express')], ondelete={'smsa': 'cascade'})


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    smsa_carrier_amount = fields.Float(
        string="SMSA Carrier Amount", default="0.0")
    smsa_cod_amount = fields.Float(string="SMSA COD Amount", default="0.0")

    def get_all_wk_carriers(self):
        res = super(StockPicking, self).get_all_wk_carriers()
        res.append('smsa')
        return res

