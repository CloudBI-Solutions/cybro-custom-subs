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
import logging
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        try:
            for order in self:
                if len(order.subscription_ids)>0:
                    latest_txs = self.env['payment.transaction'].search([('provider','=', 'stripe_checkout'),('state','=','done'),('partner_id','=',order.partner_id.id)])
                    tx = latest_txs.filtered(lambda tx: tx.reference.split('-')[0]==order.name)[0]
                    for subscription in order.subscription_ids:
                        subscription.payment_token_id = tx and tx.payment_token_id or False
                        if tx:
                            tx.subscription_id = subscription.id

        except Exception as e:
            _logger.info("........Error: while saving the payment token in the sale subscription...%r....",str(e))

        return res
