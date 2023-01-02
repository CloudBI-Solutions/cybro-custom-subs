# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
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
##########################################################################
import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from . unifonic_messaging import send_sms_using_unifonic

import logging
_logger = logging.getLogger(__name__)

class SmsMailServer(models.Model):
    """Configure the unifonic sms gateway."""

    _inherit = "sms.mail.server"
    _name = "sms.mail.server"
    _description = "unifonic Gateway"

    unifonic_appsid = fields.Char(string="Unifonic AppSid")
    unifonic_sender_id = fields.Char("Unifonic Sender Id")

    def test_conn_unifonic(self):
        self.ensure_one()
        sms_body = "unifonic Test Connection Successful........"
        mobile_number = self.user_mobile_no
        response = send_sms_using_unifonic(
            sms_body, mobile_number, sms_gateway=self)  
        _logger.info("=====%r",response)
        if response.get('success'):
            if self.sms_debug:
                _logger.info(
                    "===========Test Connection status has been sent on %r mobile number", mobile_number)
            raise UserError(_(
                "Test Connection status has been sent on %s mobile number" % mobile_number))
        if not response.get('success'):
            if self.sms_debug:
                _logger.error(
                    "==========One of the information given by you is wrong. It may be [Mobile Number] or [Api key]. Error")
            raise UserError(
                "One of the information given by you is wrong. It may be [Mobile Number] or [Api key]. Error")

    @api.model
    def get_reference_type(self):
        selection = super(SmsMailServer, self).get_reference_type()
        selection.append(('unifonic', 'Unifonic'))
        return selection
