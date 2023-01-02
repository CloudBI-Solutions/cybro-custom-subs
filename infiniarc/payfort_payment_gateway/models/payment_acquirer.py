import hashlib

from odoo import models, fields, api, _


class PayfortPaymentGateway(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(
        selection_add=[('payfort', 'Payfort')],
        ondelete={'payfort': 'set '
                             'default'})
    merchant_id = fields.Char('Merchant Identifier')
    access_code = fields.Char('Access Code')
    sha_request_phrase = fields.Char('SHA Request Phrase')
    sha_response_phrase = fields.Char('SHA Response Phrase')
    language = fields.Many2one('res.lang', string="Languages")
    lang_code = fields.Char('Language_code')
    domain = fields.Char('Domain')

    # def _get_payfort_urls(self, environment):
    #     """ payway URLs"""
    #     if environment == 'enabled':
    #         return {'payfort_form_url': 'https://checkout.payfort.com/FortAPI/paymentPage'}
    #     else:
    #         return {'payfort_form_url': 'https://sbcheckout.payfort.com/FortAPI/paymentPage'}
    #
    # def get_signature(self):
    #
    #     sha_request = self.sha_request_phrase
    #     access_code = self.access_code
    #     merchant_identifier = self.merchant_id
    #     language = self.lang_code
    #     service_command = "TOKENIZATION"
    #     merchant_reference = "ORD6"
    #
    #     request = sha_request + access_code + "=" + access_code + language + "=" + language + merchant_identifier + "=" + merchant_identifier + merchant_reference + "=" + merchant_reference + service_command + "=" + "TOKENIZATION" + sha_request
    #     shasign = hashlib.sha512(request.encode('utf-8')).hexdigest()
    #     print('shasign', shasign)
    #     return shasign

    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'payfort':
            return super()._get_default_payment_method_id()
        return self.env.ref('payfort_payment_gateway.payment_method_payfort').id


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['payfort'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res
