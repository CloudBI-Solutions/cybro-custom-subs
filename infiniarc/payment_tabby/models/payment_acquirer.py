# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from oauthlib.common import CaseInsensitiveDict

from odoo import _, api, fields, models
from odoo.exceptions import UserError
import requests
import json


class PaymentAcquirerTabby(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('tabby', 'Tabby')], ondelete={'tabby': 'set default'})
    tabby_key_public = fields.Char(string='Public Key', required_if_provider='tabby', groups='base.group_user')
    tabby_key_secret = fields.Char(string='Secret Key', required_if_provider='tabby', groups='base.group_user')
    tabby_merchant_code_25 = fields.Char(string='Merchant Code amounts less than 3000 SAR',
                                         required_if_provider='tabby', groups='base.group_user')
    tabby_merchant_code_50 = fields.Char(string='Merchant Code amounts less than 7000 SAR',
                                         required_if_provider='tabby', groups='base.group_user')

    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'tabby':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_tabby.payment_method_tabby').id


class AccountPaymentMethodTabby(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['tabby'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res
