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
import stripe
import logging
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.payment_stripe_checkout.controllers.main import StripeCheckoutController

_logger = logging.getLogger(__name__)
ZERO_DECIMAL_CURRENCIES = [
    'BIF', 'XAF', 'XPF', 'CLP', 'KMF', 'DJF', 'GNF', 'JPY', 'MGA', 'PYGí',
    'RWF', 'KRW', 'VUV', 'VND', 'XOF'
]


class TransactionStripeCheckout(models.Model):
    _inherit = 'payment.transaction'

    subscription_id = fields.Many2one('subscription.subscription', "Subscription")

    def _is_order_contain_subscription(self,data):
        try:
            reference = data.get('reference')
            order_name = reference and reference.split('-')[0] or False
            current_order = self.env['sale.order'].search([('name','=',order_name),('partner_id','=',self.partner_id.id)])
            subscription_lines = False
            if current_order:
                subscription_lines = current_order.order_line.filtered(lambda line : line.product_id.activate_subscription)
            if not reference:
                stripe_checkout_error = data.get('error', {}).get('message', '')
                _logger.error('Stripe Checkout: invalid reply received from stripe checkout API, looks like '
                              'the transaction failed. (error: %s)', stripe_checkout_error or 'n/a')
                error_msg = _("We're sorry to report that the transaction has failed.")
                if stripe_checkout_error:
                    error_msg += " " + (_("Stripe checkout gave us the following info about the problem: '%s'") %
                                        stripe_checkout_error)
                error_msg += " " + _("Perhaps the problem can be solved by double-checking your "
                                     "credit card details, or contacting your bank?")
                raise ValidationError(error_msg)
            return  current_order and subscription_lines, current_order
        except Exception as e:
            _logger.error("\n....Stripe Recurring Payment Error : Error  while checking the order subscription...%r........ ",str(e))
            return False,False

    #---------------Save the token if the order contain subscription product----------------------------------
    def _stripe_checkout_form_validate(self,  data):
        res = super(TransactionStripeCheckout,self)._stripe_checkout_form_validate(data)
        subscriptions_ids , current_order =  self._is_order_contain_subscription(data)
        if current_order and subscriptions_ids:
            # Save the payment token/card .........
            if not self.payment_token_id:
                s2s_data = {
                    'customer': data.get('customer'),
                    'payment_method': data.get('payment_method'),
                    'card': data.get('payment_method_details').get('card'),
                    'acquirer_id': self.acquirer_id.id,
                    'partner_id': self.partner_id.id,
                    'cc_name': data.get('billing_details', {}).get('name'),
                }
                if not s2s_data['cc_name']:
                    s2s_data['cc_name'] = self.partner_id.name
                token = self.acquirer_id.stripe_checkout_s2s_form_process(s2s_data)
                self.payment_token_id = token.id
                return res
            else:
                return res
        return res

    def _stripe_checkout_do_s2s_payment(self,values={}):
        self.ensure_one()
        pm_id = self.payment_token_id
        if pm_id:
            values['payment_method'] = pm_id.stripe_checkout_payment_method
        if not values.get('payment_method'):
            _logger.info("\n........Stripe Recurring Payment Error :  Paymant Method not Found...............")
            return {
                'status': False,
                'message': _("Paymant Method not Found.")
            }
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        customer_id = self.partner_id.stripe_checkout_create_customer(self.acquirer_id.id)
        success_url = StripeCheckoutController._checkout_success_url
        return_url = urls.url_join(base_url, success_url) + '?reference=%s' % self.reference
        stripe.api_key = self.acquirer_id.stripe_checkout_client_secret_key

        intent_params = {
            'amount': int(self.amount if str(self.currency_id.name) in ZERO_DECIMAL_CURRENCIES else float_round(self.amount * 100, 2)),
            'currency': self.currency_id.name,
            'off_session': 'True',
            'confirm': True,
            'payment_method': values['payment_method'],
            'customer': customer_id,
        }
        if self.acquirer_id.capture_manually:
            intent_params['capture_method'] = 'manual'
        if not pm_id:
            return {'status': False,'message': _("Paymant Token  not Found.")}

        res = self.acquirer_id._stripe_call(
            method='_payment_intent',
            operation='create',
            **intent_params
        )
        if not res['status']:
            return res
        self.stripe_checkout_payment_intent = res['response'].get('id')
        response = res.get('response') or {}
        response.update({'captured':True})
        self.state_message = "Stripe Recurring Payment Status: %s" % (response.get("status"))
        self._stripe_checkout_s2s_validate_tree(response)
        return res
