from odoo import http
from odoo.http import request


class RequestResponse(http.Controller):
    # @http.route(['/payfort_request/form'], type='http', auth="public", website=True)
    # def response(self):
    #     print('tttt')
    #     return request.render("payfort_payment_gateway.request_order_form")

    @http.route(['/response'], type='http', auth="public", methods=['POST'])
    def request_form_submit(self, **kwargs):
        print('fff')
        print('kw', kwargs)
