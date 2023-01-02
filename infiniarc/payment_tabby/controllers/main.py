import logging
import pprint

import werkzeug

from odoo import http
from odoo.http import request
import requests

_logger = logging.getLogger(__name__)


class TabbyController(http.Controller):
    _return_url = '/payment/tabby/redirect'
    _notify_url = '/payment/tabby/notify'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def tabby_return(self, **data):
        print('datas', data)
        # payment_details_id = request.env['payment.details'].search([('payment_id', '=', data['payment_id'])])
        # data = {'acquirer_id': payment_details_id.acquirer_id.id, 'provider': payment_details_id.acquirer_id.provider,
        #         'reference': payment_details_id.reference, 'amount': payment_details_id.amount,
        #         'currency_id': payment_details_id.currency_id.id, 'partner_id': payment_details_id.id}
        # _logger.info("entering _handle_feedback_data with data:\n%s", pprint.pformat(data))
        # print("sdvchgdva", data)
        data['amount'] = float(data['amount'])
        data['currency_id'] = int(data['currency_id'])
        data['partner_id'] = int(data['partner_id'])
        data['acquirer_id'] = int(data['acquirer_id'])
        request.env['payment.transaction'].sudo()._handle_feedback_data('tabby', data)
        return request.redirect('/payment/status')

    @http.route(
        _notify_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def tabby_notify(self, **data):
        # _logger.info("beginning _handle_feedback_data with post data %s", pprint.pformat(post))
        payment_details_id = request.env['payment.details'].search([('payment_id', '=', data['payment_id'])])
        data = {'acquirer_id': payment_details_id.acquirer_id.id, 'provider': payment_details_id.acquirer_id.provider,
                'reference': payment_details_id.reference, 'amount': payment_details_id.amount,
                'currency_id': payment_details_id.currency_id.id, 'partner_id': payment_details_id.id}
        _logger.info("entering _handle_feedback_data with data:\n%s", pprint.pformat(data))
        print("sdvchgdva", data)
        return werkzeug.utils.redirect('/payment/tabby/redirect?acquirer_id=%s&provider=%s&reference=%s&amount=%s&currency_id=%d&partner_id=%d' % (
            payment_details_id.acquirer_id.id, payment_details_id.acquirer_id.provider, payment_details_id.reference,
            payment_details_id.amount, payment_details_id.currency_id.id, payment_details_id.id))
        # return requests.post('/payment/tabby/redirect', data)
        # return requests.post('/payment/tabby/redirect', data)
        # return request.redirect(
        #     '/payment/tabby/redirect?acquirer_id=%s&provider=%s&reference=%s&amount=%s&currency_id=%s&partner_id=%s' % (
        #     payment_details_id.acquirer_id.id, payment_details_id.acquirer_id.provider, payment_details_id.reference,
        #     payment_details_id.amount, payment_details_id.currency_id.id, payment_details_id.id))
