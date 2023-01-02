from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class RepairRequest(http.Controller):
    @http.route('/request', type='http', auth="public", website=True)
    def repair_request(self):
        # print("first", self)
        products = request.env['product.product'].search([])
        customers = request.env['res.partner'].search([])
        values = {
            'products': products,
            'customers': customers
        }
        return request.render("repair_order.request_form", values)

    @http.route('/create/repair_request', type='http',
                auth="public", website=True)
    def request_thanks(self, **kw):
        print('looo', kw)
        customer_id = kw.get('customer_id')
        product_id = kw.get('product_id')
        print('customer', customer_id)
        print('product', product_id)
        if customer_id == '' or product_id == '':
            raise ValidationError("Please give your name and product !!!!")
        else:
            product = request.env['product.product'].search([
                ('id', '=', kw.get('product_id'))])
            product_uom_id = product.uom_id.id

            repair_data = {
                'description': kw.get('description'),
                'product_id': kw.get('product_id'),
                'product_qty': kw.get('quantity'),
                'partner_id': kw.get('customer_id'),
                'product_uom': product_uom_id,
                'state': 'draft',
                'location_id': 8,

            }
            print(repair_data)
            request.env['repair.order'].sudo().create(repair_data)
            return request.render("repair_order.request_thanks")
