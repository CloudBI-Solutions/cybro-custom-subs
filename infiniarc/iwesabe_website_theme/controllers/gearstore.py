import odoo

from odoo import http, models, tools, fields, _
from odoo.http import request
from odoo.addons.portal.controllers.web import Home
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class GearStoreType(http.Controller):
    @http.route(['/gear/<model("component.parents.type"):component>'], type='http', auth="public", website=True)
    def InfiniarcGearStoreType(self, component, page=0, **post):
        print('post............', post)
        print('component............', component)
        values = {}
        domain = [('is_published', '=', True), ('parents_type', '=', component.name)]
        brands_list = []
        if post.get('brands'):
            brands = post.get('brands').split('-')
            brands_list = [int(i) for i in brands]
            domain += [('brand_id', 'in', brands_list)]
        if post.get('component_id', False):
            component_id = int(post.get('component_id'))
            domain += [('component_id', '=', component_id)]
        if post.get('accessories_id', False):
            domain += [('public_categ_ids', '=', int(post.get('accessories_id')))]
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

        values['active_brand'] = brands_list  # request.env['brand.brand'].sudo().browse(brands_list)
        category_ids = request.env['product.public.category'].sudo().search([], order="sequence")
        values['brands'] = request.env['brand.brand'].sudo().search([])
        # values['products'] = request.env['product.product'].sudo().search(domain)
        products = request.env['product.product'].sudo().search(domain)
        url = "/products/gear_store_type"
        ppg = 18
        pager = portal_pager(url=url, total=len(products), page=page, step=ppg, url_args=post)
        current_sortby = 'Default'

        if post.get("sortby"):

            values['products'] = request.env['product.template'].sudo().search(domain, order=post.get("sortby"),
                                                                              limit=ppg, offset=pager['offset'])
            if post.get("sortby") == 'list_price asc':
                current_sortby = 'Low to High'
            elif post.get("sortby") == 'list_price desc':
                current_sortby = 'High to Low'
        else:
            print('domain............', domain)
            values['products'] = request.env['product.template'].sudo().search(domain, limit=ppg, offset=pager['offset'])
        values['pager'] = pager

        attrib_list = request.httprequest.args



        values['current_sortby'] = current_sortby
        values['search_query'] = post.get('q', False)

        values['base_component'] = request.env['component.type'].sudo().search(
            [('parents_type', '=', component.name)])
        values['component_type_parent'] = request.env['component.parents.type'].sudo().search([])

        values['website_configuration_id'] = request.env['website.configuration'].sudo().search([])

        values['active_component'] = component.id
        values['active_parts'] = request.env['component.type'].sudo().search([('parents_type', '=', component.id)],limit=1)
        print('active parts', values['active_parts'])
        keep = QueryURL('/products/gear_store_type', type=type, sortby=post.get("sortby"),
                        component_id=post.get("component_id") if post.get("component_id") else values['active_parts'].id, q=post.get("q"), price=post.get("price"))
        values['keep'] = keep
        values['filters'] = request.env['component.filter'].sudo().search([('component_id', '=', component.id)])
        return request.render("iwesabe_website_theme.gear_store_type", values)
