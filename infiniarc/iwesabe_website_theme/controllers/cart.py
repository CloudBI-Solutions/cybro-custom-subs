from odoo import http
from odoo.http import request


class AddToCart(http.Controller):
    @http.route('/ian/shop/add/cart', website=True, type='json', auth='public',
                csrf=False)
    def add_to_my_cart(self, vid, qty):
        so = request.website.sale_get_order(force_create=True)
        flag = True
        product = request.env['product.product'].search([('id', '=', vid)])
        for rec in so.order_line:
            if vid == rec.product_id.id:
                rec.product_uom_qty += qty
                flag = False
                break

        if flag:
            so.write(
                {'order_line': [
                    (0, 0, {
                        'name': product.name,
                        'product_id': product.id,
                        'product_uom_qty': 1,
                        'price_unit': product.list_price,
                        'tax_id': False,
                    })]}
            )

    @http.route('/website/shop', website=True, auth="public", type='json')

    def website_configuration(self):

        print('webste_configuration...........')

        values = {}
        qty = request.env['website.configuration'].sudo().search([])
        values['qty'] = qty.cart_qty_limit
        print('quantity value', values)

        return values