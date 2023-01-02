import odoo

from odoo import http, models, tools, fields, _
from odoo.http import request
# from odoo.addons.website_sale_wishlist.controllers import WebsiteSaleWishlist
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import fields, http, SUPERUSER_ID, tools, _
import json


class InfiniarcWishList(WebsiteSale):
    @http.route(['/shop/wishlist'], type='http', auth="public", website=True, sitemap=False)
    def get_wishlist(self, count=False, **kw):
        values = request.env['product.wishlist'].with_context(display_default_code=False).current()
        if count:
            return request.make_response(json.dumps(values.mapped('product_id').ids))

        if not len(values):
            return request.redirect("/")

        return request.render("website_sale_wishlist.product_wishlist", dict(wishes=values))

