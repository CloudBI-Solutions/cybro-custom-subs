# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
import logging
from datetime import datetime

# from ..models.braintree_connector import BraintreeConnector
from odoo import api, fields, models, tools, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare

_logger = logging.getLogger(__name__)

class TransactionBraintreeIinherit(models.Model):
    _inherit = 'payment.transaction'

    def _braintree_form_validate(self, data):
        status = data.get('status')
        payment_token = self.payment_token_id
        res = {
            'brt_txnid': data.get('acquirer_reference'),
            'acquirer_reference': data.get('acquirer_reference'),
            'state_message': data.get('tx_msg'),
            'brt_txcurrency': data.get('currency'),
            
        }
        if not self.payment_token_id:
            payment_token = self.env['payment.token'].sudo().create({
                'acquirer_id':self.acquirer_id.id,
                'acquirer_ref':data.get('acquirer_reference'),
                'partner_id':self.partner_id.id
            })   
            res.update({
                'payment_token_id':payment_token.id
            })
            
        if status:
            _logger.info('Validated Braintree payment for tx %s: set as done' % (self.reference))
            self._set_transaction_done()
            
        invoice_ids = self.invoice_ids
        if invoice_ids:
            invoices = self.env['account.move'].sudo().search([('invoice_line_ids.subscription_id', '!=',False),('id','in',invoice_ids.ids)])
            for invoice in invoices:
                for line in invoice.invoice_line_ids:
                    if line.subscription_id and line.subscription_id.braintree_payment_mode == 'recurring' and not line.subscription_id.payment_token_id and payment_token:
                        line.subscription_id.payment_token_id = payment_token.id
        
        return self.write(res)
        
        
