# from werkzeug.exceptions import NotFound
from odoo import http, models, tools, fields, _
from odoo.http import Controller, request, route, content_disposition
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.auth_signup.models.res_users import SignupError
import logging
import werkzeug
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class FilterController(http.Controller):

    @http.route(['/desk/<model("product.filter"):filter>'], type='http', auth="public", website=True)
    def product_filter_view(self, filter, **post):
        values = {}
        values['filter'] = request.env['product.filter'].sudo().search([])
        values['name'] = filter.filter

        models = request.env['desktop.filter'].sudo().search([])
        brands = request.env['brand.brand'].sudo().search([])
        gpus = request.env['gpu.gpu'].sudo().search([])
        values['gpus'] = []
        values['brands'] = []
        values['models'] = []
        # for gpu in gpus:
        #     values['gpus'].append(gpu)
        for model in models:
            values['models'].append(model)
        # for brand in brands:
        #     values['brands'].append(brand)

        domain = [('filter_type', 'in', filter.ids), ('is_published', '=', True)]
        brands_list = []
        if post.get('q', False):
            domain += [('name', 'ilike', post.get('q', False))]

        if post.get('price', False):
            price = post.get('price', False).split("-")
            values.update({
                'min_price': price[0],
                'max_price': price[1]
            })
            if price[0]:
                domain += [('list_price', '>=', int(price[0]))]
            if price[1]:
                domain += [('list_price', '<=', int(price[1]))]
        if post.get('brands'):
            brands = post.get('brands').split('-')

            brands_list = [int(i) for i in brands]

            domain += [('brand_id', 'in', brands_list)]

        values['active_brand'] = brands_list

        customize_products = request.env['product.template'].sudo().search(domain)

        url = ""
        ppg = 18

        pager = portal_pager(url=url, total=len(customize_products), step=ppg, url_args=post)
        current_sortby = 'Default'
        if post.get("sortby"):
            if post.get("sortby") == 'list_price asc':
                current_sortby = 'Low to High'
            elif post.get("sortby") == 'list_price desc':
                current_sortby = 'High to Low'
            values['customize_products'] = request.env['product.template'].sudo().search(domain,
                                                                                        order=post.get("sortby"),
                                                                                        limit=ppg,
                                                                                        offset=pager['offset'])
        else:
            values['customize_products'] = request.env['product.template'].sudo().search(domain, limit=ppg,
                                                                                        offset=pager['offset'])

        values['pager'] = pager

        keep = QueryURL('products', sortby=post.get("sortby"), brands=post.get('brands'), gpus=post.get('gpus'),
                        models=post.get('models'), price=post.get('price'),
                        q=post.get("q"))

        values['active_filter'] = filter.id
        values['keep'] = keep
        values['current_sortby'] = current_sortby
        values['search_query'] = post.get('q', False)
        values['filters'] = request.env['desktop.filter'].sudo().search([('type', '=', filter.filter)])

        return request.render("iwesabe_website_theme.gaming_pc", values)

