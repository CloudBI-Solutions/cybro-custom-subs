import pprint
from werkzeug import urls
import time
from odoo import _, api, models, fields
from odoo.exceptions import ValidationError, _logger, UserError
# from multisafepay.client import Client
from datetime import date, datetime, time

from oauthlib.common import CaseInsensitiveDict

import requests
import json
from odoo.addons.payment_tabby.controllers.main import TabbyController


class TabbyTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super(TabbyTransaction, self)._get_specific_rendering_values(processing_values)

        if self.provider != 'tabby':
            return res
        url = "https://api.tabby.ai/api/v2/checkout"

        return_url = urls.url_join(self.acquirer_id.get_base_url(), TabbyController._return_url)
        notify_url = urls.url_join(self.acquirer_id.get_base_url(), TabbyController._notify_url)

        # headers = CaseInsensitiveDict()
        acquirer_id = self.env['payment.acquirer'].search([('provider', '=', 'tabby')])
        reference = processing_values['reference'].split("-")
        currency = self.env['res.currency'].search([('id', '=', processing_values['currency_id'])])
        partner = self.env['res.partner'].search([('id', '=', processing_values['partner_id'])])
        order = self.env['sale.order'].search([('name', '=', reference[0])])
        items = []
        merchant_code = ''
        print('order', order.order_line.product_id)

        # if order.order_line.product_id
        if processing_values['amount'] <= 3000:
            merchant_code = acquirer_id.tabby_merchant_code_25
        elif 3000 <= processing_values['amount'] <= 7000:
            merchant_code = acquirer_id.tabby_merchant_code_50
        print('merchant_code', merchant_code)
        # for new in order.order_line.product_id:
        #     if new.tabby != True:
        #         print('''''vvvvvvvv''')
        #         raise UserError(
        #             _("There is already a shared filter set as default for  delete or change it before setting a new default"))
        for line in order.order_line:
            for order in line.product_id:
                if order.tabby == False:
                    raise ValidationError(
                        _("Some of the ordered products are not supporting the tabby payment method"))

            # else:
            item = {
                "title": line.product_id.name,
                "description": line.name,
                "quantity": int(line.product_uom_qty),
                "unit_price": line.price_unit,
                "discount_amount": "0.00",
                "reference_id": processing_values['reference'],

                "gender": "Male",
                "category": line.product_id.categ_id.name,
                "color": "string",
                "product_material": "string",
                "size_type": "string",
                "size": "string",
                "brand": "string"
            }
            items.append(item)
        print('item', items)

        data = {
            "payment": {
                "amount": processing_values['amount'],
                "currency": "SAR",
                "description": processing_values['reference'],
                "buyer": {
                    "phone": partner.phone,
                    "email": partner.email,
                    "name": partner.name,
                    # "dob": partner.dob,
                },
                "shipping_address": {
                    "city": partner.city,
                    "address": partner.street,
                    "zip": partner.zip,
                },
                "order": {
                    "tax_amount": "0.00",
                    "shipping_amount": "0.00",
                    "discount_amount": "0.00",
                    "updated_at": "2019-08-24T14:15:22Z",
                    "reference_id": "656453456789",
                    "items": items

                },

            },
            "lang": "ar",
            "merchant_code": merchant_code,
            "merchant_urls": {
                "success": notify_url,
                # "cancel": "https://your-store/cancel",
                # "failure": "https://your-store/failure"
            }
        }
        key = acquirer_id.tabby_key_public

        headers = {"Authorization": "Bearer " + key,
                   "Content-Type": "application/json"}

        resp = requests.post(url, headers=headers, data=json.dumps(data))
        response = resp.json()
        print('resp.json()[configuration][available_products]', resp.json())
        response['api_url'] = str(resp.json()['configuration']['available_products']['installments'][0]['web_url'])
        response['apiKey'] = key
        response['Product'] = 'installments'
        response['merchantCode'] = acquirer_id.tabby_merchant_code_25
        response['return_url'] = return_url
        payment_details_id = self.env['payment.details'].create({
            'acquirer_id': processing_values['acquirer_id'],
            'reference': processing_values['reference'],
            'amount': processing_values['amount'],
            'currency_id': processing_values['currency_id'],
            'partner_id': processing_values['partner_id'],
            'payment_id': response['payment']['id']
        })
        capture_url = 'https://api.tabby.ai/api/v1/payments/{%s}/captures' % (payment_details_id['payment_id'])
        capture_data = {
            "amount": processing_values['amount'],
            "tax_amount": "0.00",
            "shipping_amount": "0.00",
            "discount_amount": "0.00",
            "created_at": "string",
            "items": items
        }
        now = datetime.now()
        close_url = 'https://api.tabby.ai/api/v1/payments/{%s}/close' % (payment_details_id['payment_id'])
        close_data = {
            "id": payment_details_id['payment_id'],
            "created_at": str(now),
            # "expires_at": "2019-08-24T14:15:22Z",
            "status": "CREATED",
            "is_test": True,
            "amount": processing_values['amount'],
            "currency": "SAR",
            "description": "string",

            "order": {
                "tax_amount": "0.00",
                "shipping_amount": "0.00",
                "discount_amount": "0.00",
                "updated_at": "2019-08-24T14:15:22Z",
                "reference_id": "string",
                "items": items
            },

        }
        key_secret = acquirer_id.tabby_key_secret
        capture_headers = {"Authorization": "Bearer " + key_secret,
                           "Content-Type": "application/json"}

        capture_resp = requests.post(url, headers=capture_headers, data=json.dumps(capture_data))
        close_resp = requests.post(url, headers=capture_headers, data=json.dumps(close_data))

        capture_response = capture_resp.json()
        close_response = close_resp.json()
        return response

    @api.model
    def _get_tx_from_feedback_data(self, provider, data):

        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'tabby':
            return tx

        reference = data.get('reference')
        tx = self.search([('reference', '=', reference), ('provider', '=', 'tabby')])
        if not tx:
            raise ValidationError(
                "Tabby: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_feedback_data(self, data):
        print('selfwe', self)
        print('dataaaaa', data)
        super()._process_feedback_data(data)
        if self.provider != 'tabby':
            return
        else:
            self._set_done()


class PaymentDetails(models.TransientModel):
    _name = 'payment.details'

    acquirer_id = fields.Many2one('payment.acquirer')
    reference = fields.Char()
    amount = fields.Float()
    currency_id = fields.Many2one('res.currency')
    partner_id = fields.Many2one('res.partner')
    payment_id = fields.Char()


