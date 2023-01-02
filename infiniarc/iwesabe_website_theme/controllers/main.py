# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import hashlib

import requests
import werkzeug

from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing
from odoo.fields import Command
import odoo
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment.controllers.portal import PaymentPortal

from odoo import http, models, tools, fields, _
from odoo.http import request
import datetime
from dateutil.relativedelta import relativedelta
import warnings
from odoo.addons.portal.controllers.web import Home
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager
import math, json, random
from odoo.exceptions import AccessError, UserError, ValidationError

from datetime import date, datetime, time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TableCompute(object):

    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey, ppr):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= ppr:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(ppr):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, products, ppg=20, ppr=4):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        for p in products:
            x = min(max(p.website_size_x, 1), ppr)
            y = min(max(p.website_size_y, 1), ppr)
            if index >= ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(pos % ppr, pos // ppr, x, y, ppr):
                pos += 1
            # if 21st products (index 20) and the last line is full (ppr products in it), break
            # (pos + 1.0) / ppr is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= ppg and ((pos + 1.0) // ppr) > maxy:
                break

            if x == 1 and y == 1:  # simple heuristic for CPU optimization
                minpos = pos // ppr

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
            self.table[pos // ppr][pos % ppr] = {
                'product': p, 'x': x, 'y': y,
                'ribbon': p._get_website_ribbon(),
            }
            if index <= ppg:
                maxy = max(maxy, y + (pos // ppr))
            index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]

        return rows


class Website(Home):

    @http.route('/', type='http', auth="public", website=True, sitemap=True)
    def index(self, **kw):
        value = {}
        top_menu = request.website.menu_id
        homepage = request.website.homepage_id
        value['our_partners'] = request.env['our.partner'].sudo().search([('website_published', '=', True)])
        value['gear_store_products'] = request.env['product.template'].sudo().search(
            [('is_gear_store', '=', True), ('is_published', '=', True)])
        # value['best'] = request.env['product.template'].sudo().search([('best', '=', True)])
        best_sellers = request.env['product.template'].sudo().search([])
        value['best_sellers'] = best_sellers.filtered(
            lambda s: (s.is_published == True and s.best_seller == True) or (s.arrival == True))
        # value['best_sellers'] = request.env['product.template'].sudo().search(
        #     [('is_published', '=', True), ('best_seller', '=', True) or ('arrival', '=', True)])
        print('best_sellers', value['best_sellers'])
        value['component'] = request.env['component.type'].sudo().search([('parents_type', '=', 'Accessories')],
                                                                         limit=2)
        value['component_base'] = request.env['component.type'].sudo().search([('parents_type', '=', 'Base component')],
                                                                              limit=2)
        value['models'] = request.env['product.filter'].sudo().search([])
        value['configuration_id'] = request.env['website.configuration'].sudo().search([], limit=1)
        value['announcements'] = request.env['infiniarc.announcement'].sudo().search([])
        value['banner'] = request.env['home.banner'].sudo().search([('show', '=', True)])
        value['small_banner'] = request.env['home.small.banner'].sudo().search([('show', '=', True)])
        value['banner_slider'] = request.env['home.banner.slider'].sudo().search([('show', '=', True)])
        print('announcements:', value['announcements'])
        print('banner:', value['banner'])
        value['gearstore'] = request.env['component.parents.type'].sudo().search([])

        if homepage and (
                homepage.sudo().is_visible or request.env.user.has_group('base.group_user')) and homepage.url != '/':
            return request.env['ir.http'].reroute(homepage.url)
        website_page = request.env['ir.http']._serve_page()
        if website_page:
            value['posts'] = request.env['blog.post'].sudo().search([], limit=6)
            value['configuration_id'] = request.env['website.configuration'].sudo().search([], limit=1)
            value['component_type_parent'] = request.env['component.parents.type'].sudo().search([])

            return request.render('iwesabe_website_theme.infiniarc_index', value)
        else:
            first_menu = top_menu and top_menu.child_id and top_menu.child_id.filtered(lambda menu: menu.is_visible)
            if first_menu and first_menu[0].url not in ('/', '', '#') and (
                    not (first_menu[0].url.startswith(('/?', '/#', ' ')))):
                # return request.redirect('/', 303)
                return request.redirect(first_menu[0].url)
        # raise request.not_found()
        return request.render('iwesabe_website_theme.infiniarc_index', value)
        # return request.redirect('/', 303)


class WebsiteInfiniarc(http.Controller):

    @http.route('/shop/payment', type='http', auth="public", website=True)
    def InfiniarcCustomCheckout(self, **post):
        order = request.website.sale_get_order()
        countries = request.env['res.country'].sudo().search([])
        logged_in = not request.env.user._is_public()
        acquirers_sudo = request.env['payment.acquirer'].sudo()._get_compatible_acquirers(
            order.company_id.id,
            order.partner_id.id,
            currency_id=order.currency_id.id,
            sale_order_id=order.id,
            website_id=request.website.id,
        )
        tokens = request.env['payment.token'].search(
            [('acquirer_id', 'in', acquirers_sudo.ids), ('partner_id', '=', order.partner_id.id)]
        ) if logged_in else request.env['payment.token']
        fees_by_acquirer = {
            acq_sudo: acq_sudo._compute_fees(
                order.amount_total, order.currency_id, order.partner_id.country_id
            ) for acq_sudo in acquirers_sudo.filtered('fees_active')
        }
        # Prevent public partner from saving payment methods but force it for logged in partners
        # buying subscription products
        show_tokenize_input = logged_in \
                              and not request.env['payment.acquirer'].sudo()._is_tokenization_required(
            sale_order_id=order.id
        )
        values = {
            'website_sale_order': order,
            'acquirers': acquirers_sudo,
            'tokens': tokens,
            'fees_by_acquirer': fees_by_acquirer,
            'show_tokenize_input': show_tokenize_input,
            'countries': countries
        }
        return request.render("iwesabe_website_theme.infiniarc_custom_new_checkout", values)

    @http.route([
        '''/gaming-desktops''',
        '''/gaming-desktops/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def GamingPc(self, page=0, **post):

        values = {'filters': request.env['desktop.filter'].sudo().search([])}
        url = http.request.httprequest.full_path
        str_list = url[url.find('[') + 1: url.find(']')]
        domain = [('is_published', '=', True)]
        price_filter_list = url[url.find('&{') + 2: url.find('&}')].replace(
            'NaN', '0')
        try:
            price_filters = [int(num) for num in price_filter_list.split(',')]
            if price_filters[0] > 0:
                values['min_price'] = price_filters[0]
                domain += [('list_price', '>=', price_filters[0])]
            if price_filters[1] > 0:
                values['max_price'] = price_filters[1]
                domain += [('list_price', '<=', price_filters[0])]
        except:
            print('No Price Filter Product')

        f_flag = False
        values = {'filters': request.env['desktop.filter'].sudo().search([])}

        try:
            filter_list = [int(num) for num in str_list.split(',')]
            values['cur_filters'] = filter_list
            f_flag = True
            domain += [('value_id', 'in', filter_list)]
            print('helloooo', filter_list)
        except:
            print('No Filter')

        brands_list = []
        values['f_flag'] = f_flag

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

        customize_products = request.env['product.template'].sudo().search(
            domain)

        url = "/gaming-desktops"
        ppg = 18
        pager = portal_pager(url=url, total=len(customize_products), page=page,
                             step=ppg, url_args=post)
        current_sortby = 'Default'

        if post.get("order"):
            if post.get("order") == 'list_price asc':
                current_sortby = 'Low to High'
            elif post.get("order") == 'list_price desc':
                current_sortby = 'High to Low'

            values['customize_products'] = request.env[
                'product.template'].sudo().search(domain, limit=ppg,
                                                  offset=pager['offset'],
                                                  order=post.get("order"))
            print(values)
        else:
            values['customize_products'] = request.env[
                'product.template'].sudo().search(domain, limit=ppg,
                                                  offset=pager['offset'])
        values['pager'] = pager

        keep = QueryURL('products', sortby=post.get("order"),
                        brands=post.get('brands'), price=post.get('price'),
                        q=post.get("q"))
        values['keep'] = keep
        # values['customize_products'] = request.env[
        #     'product.template'].sudo().search([('parents_type', '!=', False)])

        values['active_filter'] = 0
        values['current_sortby'] = current_sortby
        values['search_query'] = post.get('q', False)
        return request.render("iwesabe_website_theme.gaming_pc_view", values)

    @http.route('/get_gaming_desktop_view', type='http', website=True,
                auth="public", csrf=False)
    def GamingPcView(self, page=0, **post):
        print('post gpc', post)
        print('Hellooo hkjhshkjf')
        url = "/gaming-desktops"
        ppg = 18
        domain = [('is_published', '=', True)]

        if post.get('component_id', False):
            component_id = int(post['component_id'])
            domain += [('component_id', '=', component_id)]

        if post.get('q', False):
            domain += [('name', 'ilike', post.get('q', False))]

        if post.get('price', False):
            price = post.get('price', False).split("-")
            if price[0]:
                domain += [('list_price', '>=', int(price[0]))]
            if price[1]:
                domain += [('list_price', '<=', int(price[1]))]

        if post.get('models'):
            print('mofdelsss')
            models = post.get('models').split('-')
            models_list = [int(i) for i in models]
            domain += [('value_id', 'in', models_list)]

        products_count = request.env['product.template'].sudo().search_count(domain)
        pager = portal_pager(url=url, total=products_count, page=page, step=ppg, url_args=post)
        products = request.env['product.template'].sudo().search(domain, limit=ppg, offset=pager['offset'])
        View_Products = request.env['ir.ui.view']._render_template('iwesabe_website_theme.gaming_pc_product_template', {
            'customize_products': products,
            'pager': pager,
        })
        return View_Products

    @http.route('/get_gearstore_view', type='http', auth="public", csrf=False)
    def GearStoreView(self, page=0, **post):
        url = "/gaming-desktops"
        ppg = 18
        domain = [('is_published', '=', True)]
        if post.get('q', False):
            domain += [('name', 'ilike', post.get('q', False))]
        if post.get('price', False):
            price = post.get('price', False).split("-")
            if price[0]:
                domain += [('list_price', '>=', int(price[0]))]
            if price[1]:
                domain += [('list_price', '<=', int(price[1]))]

        if post.get('models'):
            models = post.get('models').split('-')
            models_list = [int(i) for i in models]
            domain += [('model_ids', 'in', models_list)]

        products_count = request.env['product.product'].sudo().search_count(
            domain)
        pager = portal_pager(url=url, total=products_count, page=page, step=ppg,
                             url_args=post)
        product = request.env['component.filter'].sudo().search([])
        # products = []
        for new in product.product_ids:
            # v = int(post.get('models'))
            for abc in models_list:
                if new.id == abc:
                    products = new.product_id
                    # products = request.env['product.product'].sudo().search(domain, limit=ppg, offset=pager['offset'])
                    # View_Products = request.env['ir.ui.view']._render_template('iwesabe_website_theme.gaming_pc_product_template', {
                    View_Products = request.env['ir.ui.view']._render_template(
                        'iwesabe_website_theme.product_list_view', {
                            'products': products,
                            'pager': pager,
                        })
                    return View_Products

    @http.route('/products/gear_store', type='http', auth="public", website=True)
    def GearStore(self, **post):
        values = {}
        category_ids = request.env['product.public.category'].sudo().search([], order="sequence")
        values['component_type_parent'] = request.env['component.parents.type'].sudo().search([])
        values['component'] = request.env['component.type'].sudo().search([])
        if category_ids:
            values['main_category'] = category_ids[0] if category_ids[0] else False
            values['side_categories'] = category_ids[1:5] if category_ids[1:5] else False
            values['another_categories'] = category_ids[5:] if category_ids[5:] else False
        values['brands'] = request.env['brand.brand'].sudo().search([])

        values['website_configuration_id'] = request.env['website.configuration'].sudo().search([])
        return request.render("iwesabe_website_theme.gear_store", values)

    @http.route(['''/special_offer''', '''/special_offer/page/<int:page>'''], type='http', auth="public", website=True)
    def SpecialOffer(self, page=0, **post):
        print('post............', post)
        values = {}
        domain = [('is_published', '=', True)]
        brands_list = []
        models = request.env['product.model'].sudo().search([])
        brands = request.env['brand.brand'].sudo().search([])
        gpus = request.env['gpu.gpu'].sudo().search([])
        values['gpus'] = []
        values['brands'] = []
        values['models'] = []
        for gpu in gpus:
            values['gpus'].append(gpu)
        for model in models:
            values['models'].append(model)
        for brand in brands:
            values['brands'].append(brand)

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

        products = request.env['product.product'].sudo().search([])
        values['brands'] = request.env['brand.brand'].sudo().search([])
        url = "/special_offer"
        ppg = 10

        values['pager'] = portal_pager(url=url, total=len(products), page=page, step=ppg, url_args=post)
        #
        values['active_offer'] = 0
        values['offer'] = request.env['special.offer'].sudo().search([])
        values['products'] = request.env['product.template'].sudo().search([('special_offer', '=', True)])
        return request.render("iwesabe_website_theme.special_offer", values)

    @http.route(['''/special/<model("special.offer"):offers>''',
                 '''/special/<model("special.offer"):offers>/page/<int:page>'''], type='http', auth="public",
                website=True)
    def SpecialOfferType(self, offers, page=0, **post):
        print('offerrrrss', offers.name)
        print('SpecialOfferType offerpost', post)
        values = {}
        domain = [('special_offer', '=', True), ('is_published', '=', True)]
        if offers.name == 'Gaming Pc':
            domain += [('filter_type', '!=', False)]
        elif offers.name == 'Gear Store':
            domain += [('parents_type', '!=', False)]
        elif offers.name == 'Stock Clearance':
            domain += [('stock_clearance', '=', True)]
        else:
            domain += []
        products = request.env['product.product'].sudo().search([])
        url = "/special_offer"
        ppg = 18
        values['pager'] = portal_pager(url=url, total=len(products), page=page, step=ppg, url_args=post)
        #
        values['offer'] = request.env['special.offer'].sudo().search([])
        values['active_offer'] = offers.id
        values['filters'] = request.env['special.filter'].sudo().search([('type', '=', offers.name)])
        print('filters....', values['filters'])
        values['products'] = request.env['product.template'].sudo().search(domain)
        return request.render("iwesabe_website_theme.special_offer", values)

    @http.route([
        '''/products/gear_store_type''',
        '''/products/gear_store_type/page/<int:page>'''
    ], type='http', auth="public", csrf=False, website=True)
    def GearStoreType(self, page=0, type='base-components', **post):
        print('post***', post)
        print('post.get(component_id)', post.get('component_id'))
        values = {}
        domain = [('is_published', '=', True)]
        url = http.request.httprequest.full_path
        price_filter_list = url[url.find('&{') + 2: url.find('&}')].replace('NaN', '0')
        try:
            price_filters = [int(num) for num in price_filter_list.split(',')]
            if price_filters[0] > 0 :
                values['min_price'] = price_filters[0]
                domain += [('list_price', '>=', price_filters[0])]
            if price_filters[1] > 0:
                values['max_price'] = price_filters[1]
                domain += [('list_price', '<=', price_filters[0])]
        except:
            print('No Price Filter Product')

        print('post.get(component_id)', post.get('component_id'))
        brands_list = []
        models = request.env['product.product'].sudo().search([])
        brands = request.env['brand.brand'].sudo().search([])
        gpus = request.env['gpu.gpu'].sudo().search([])
        values['gpus'] = []
        values['brands'] = []
        values['models'] = []
        for gpu in gpus:
            values['gpus'].append(gpu)
        for model in models:
            values['models'].append(model)
        for brand in brands:
            values['brands'].append(brand)

        if post.get('brands'):
            brands = post.get('brands').split('-')
            brands_list = [int(i) for i in brands]
            domain += [('brand_id', 'in', brands_list)]
        if post.get('component_id', False):
            component_id = request.env['component.type'].sudo().search([('id', '=', post.get('component_id'))])
            print('component_id1', component_id)
            domain += [('component_id', '=', component_id.id)]
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
        products = request.env['product.template'].sudo().search(domain)
        url = "/products/gear_store_type"
        ppg = 18
        pager = portal_pager(url=url, total=len(products), page=page, step=ppg, url_args=post)
        current_sortby = 'Default'

        if post.get("order"):
            values['products'] = request.env['product.template'].sudo().search(
                domain, order=post.get("order"),
                limit=ppg, offset=pager['offset'])
            if post.get("order") == 'list_price asc':
                current_sortby = 'Low to High'
            elif post.get("order") == 'list_price desc':
                current_sortby = 'High to Low'
        else:
            values['products'] = request.env['product.template'].sudo().search(
                domain, limit=ppg,
                offset=pager['offset'])
        values['pager'] = pager

        attrib_list = request.httprequest.args

        keep = QueryURL('/products/gear_store_type', type=type,
                        sortby=post.get("order"),
                        component_id=post.get("component_id"), q=post.get("q"),
                        price=post.get("price"))
        values['keep'] = keep
        values['current_sortby'] = current_sortby
        values['search_query'] = post.get('q', False)
        component_id = post.get('component_id')
        print('component_id', component_id)
        # component_id =

        # component_id = int(component_id) if component_id else ''
        component = request.env['component.type'].sudo().browse(int(component_id))
        values['base_component'] = request.env['component.type'].sudo().search(
            [('parents_type', '=', component.parents_type.id)])

        values['component_type_parent'] = request.env['component.parents.type'].sudo().search([])
        values['active_component'] = component.parents_type.id
        values['active_parts'] = component.id
        print('active_parts', component.name)
        values['filters'] = request.env['component.filter'].sudo().search([('component_id', '=', component.name)])
        print('filters', values['filters'])
        return request.render("iwesabe_website_theme.gear_store_type", values)

    @http.route('/get_gear_store_type_view', type='http', auth="public", csrf=False)
    def GearStoreTypeView(self, page=0, **post):
        values = {}
        domain = []
        if post.get('brands'):
            brands = post.get('brands').split('-')
            brands_list = [int(i) for i in brands]
            domain += [('brand_id', 'in', brands_list)]
        # domain += [('brand_id','=',int(post.get('brands')))]
        if post.get('component_id', False):
            component_id = int(post.get('component_id'))
            domain += [('component_id', '=', component_id)]
        if post.get('accessories_id', False):
            domain += [('public_categ_ids', '=', int(post.get('accessories_id')))]
        if post.get('q', False):
            domain += [('name', 'ilike', post.get('q', False))]
        if post.get('price', False):
            price = post.get('price', False).split("-")
            if price[0]:
                domain += [('list_price', '>=', int(price[0]))]
            if price[1]:
                domain += [('list_price', '<=', int(price[1]))]

        url = "/products/gear_store_type"
        ppg = 18

        products_count = request.env['product.product'].sudo().search_count(domain)
        pager = portal_pager(url=url, total=products_count, page=page, step=ppg, url_args=post)
        products = request.env['product.product'].sudo().search(domain, limit=ppg, offset=pager['offset'])
        View_Products = request.env['ir.ui.view']._render_template('iwesabe_website_theme.product_list_view', {
            'products': products,
            'pager': pager,
        })

        return View_Products

    @http.route(['/store/<model("product.product"):product_id>'], type='http', auth="public", website=True)
    def StoreCustomizeProduct(self, product_id, **post):

        values = {
            'product_id': product_id.product_tmpl_id,
        }
        return request.render("iwesabe_website_theme.product_customize", values)

    # update needed for this route parameter
    @http.route(['/shop/cart/update_components'], type='json', auth="public",
                methods=['GET', 'POST'], website=True,
                csrf=False)
    def cart_update(self, product_ids, customization=False,
                    components_dict=False, add_qty=1, set_qty=0,
                    product_custom_attribute_values=None, **kw):
        print(product_ids, 'mew')
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        # product_custom_attribute_values = None
        if product_custom_attribute_values:
            product_custom_attribute_values = json.loads(product_custom_attribute_values)

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(kw.get('no_variant_attribute_values'))

        if sale_order:

            for product_id in product_ids:
                try:
                    product_id = int(product_id)
                except:
                    pass
                sale_order._cart_update(
                    product_id=int(product_id),
                    add_qty=add_qty,
                    set_qty=set_qty,
                    product_custom_attribute_values=product_custom_attribute_values,
                    no_variant_attribute_values=no_variant_attribute_values,
                )
            return True
        else:
            return False

    #
    @http.route('/shop/payment', type='http', auth="public", website=True)
    def InfiniarcCustomCheckout(self, **post):
        print('post', post)
        order = request.website.sale_get_order()
        print('reaad', order.read())
        print('amount_del', order.carrier_price)
        partner_id = order.partner_id
        payfort = request.env['payment.acquirer'].sudo().search([('provider', '=', 'payfort')])
        countries = request.env['res.country'].sudo().search([])
        outlets = request.env['company.outlets'].sudo().search([])
        # 'access_token': order._portal_ensure_token(),
        # 'transaction_route': f'/shop/payment/transaction/{order.id}',
        # 'landing_route': '/shop/payment/validate',
        access_token = order._portal_ensure_token()

        logged_in = not request.env.user._is_public()
        acquirers_sudo = request.env['payment.acquirer'].sudo().search(
            [('state', 'in', ('enabled', 'test')), ('company_id', '=', order.company_id.id)])
        print('acquirers_sudo', acquirers_sudo)
        #     _get_compatible_acquirers(
        #     order.company_id.id,
        #     order.partner_id.id,
        #     currency_id=order.currency_id.id,
        #     sale_order_id=order.id,
        #     website_id=request.website.id,
        # )
        print('sudo', acquirers_sudo)
        tokens = request.env['payment.token'].search(
            [('acquirer_id', 'in', acquirers_sudo.ids), ('partner_id', '=', order.partner_id.id)]
        ) if logged_in else request.env['payment.token']
        print('tokens', tokens)
        fees_by_acquirer = {
            acq_sudo: acq_sudo._compute_fees(
                order.amount_total, order.currency_id, order.partner_id.country_id
            ) for acq_sudo in acquirers_sudo.filtered('fees_active')
        }
        print('fee', fees_by_acquirer)
        # Prevent public partner from saving payment methods but force it for logged in partners
        # buying subscription products
        show_tokenize_input = logged_in \
                              and not request.env['payment.acquirer'].sudo()._is_tokenization_required(
            sale_order_id=order.id
        )
        transaction = request.env['payment.transaction'].sudo().search([])
        # transaction = request.env['payment.transaction'].sudo().search([])[0]
        randnumb = str(random.getrandbits(16))
        for trans in transaction:
            reference = str(trans.reference) + randnumb
        sha_request = str(payfort.sha_request_phrase)
        access_code_id = str(payfort.access_code)
        merchant_identifier_id = str(payfort.merchant_id)
        language_code = str(payfort.lang_code)
        service_command_type = "TOKENIZATION"
        return_url = "/payfort/response"
        domain = payfort.domain
        return_url_val = str(domain) + return_url
        token_request = sha_request + "access_code" + "=" + access_code_id + "language" + "=" + language_code + "merchant_identifier" + "=" + merchant_identifier_id + "merchant_reference" + "=" + reference + "return_url" + "=" + return_url_val + "service_command" + "=" + service_command_type + sha_request
        shasign = hashlib.sha256(token_request.encode('utf-8')).hexdigest()
        print(shasign)
        print('tok', token_request)

        values = {
            'website_sale_order': order,
            'acquirers': acquirers_sudo,
            'tokens': tokens,
            'fees_by_acquirer': fees_by_acquirer,
            'show_tokenize_input': show_tokenize_input,
            'countries': countries,
            'partner': partner_id,
            'outlets': outlets,
            'payfort': payfort,
            'shasign': shasign,
            'return_url': return_url_val,
            'reference': reference,
            'access_token': order._portal_ensure_token(),
            'transaction_route': f'/shop/payment/transaction/{order.id}',
            'landing_route': '/shop/payment/validate',
        }
        print(values)
        return request.render("iwesabe_website_theme.infiniarc_custom_new_checkout", values)

    @http.route('/payfort/response', type='http', auth="public", website=True, csrf=False, )
    def PayfortResponse(self, **kw):
        order = request.website.sale_get_order()
        payfort = request.env['payment.acquirer'].sudo().search([('provider', '=', 'payfort')])

        sha_request = payfort.sha_request_phrase
        access_code_id = kw['access_code']
        merchant_identifier_id = kw['merchant_identifier']
        merchant_reference_val = kw['merchant_reference']
        language_code = kw['language']
        service_command_type = "PURCHASE"
        amount_val = str(int(order.amount_total))
        currency_val = "SAR"
        customer_email_val = order.partner_id.email
        token_name_val = kw['token_name']
        customer_ip_addr = "192.178.1.10"
        customer = kw['card_holder_name']
        return_url = "/payfort/response/message"
        domain = payfort.domain
        return_url_val = domain + return_url

        token_request = sha_request + "access_code" + "=" + access_code_id + "amount" + "=" + amount_val + "command" + "=" + service_command_type + "currency" + "=" + currency_val + "customer_email" + "=" + customer_email_val + "customer_ip" + "=" + customer_ip_addr + "language" + "=" + language_code + "merchant_identifier" + "=" + merchant_identifier_id + "merchant_reference" + "=" + merchant_reference_val + "return_url" + "=" + return_url_val + "token_name" + "=" + token_name_val + sha_request
        shasignature = hashlib.sha256(token_request.encode('utf-8')).hexdigest()
        print(shasignature)
        print('tok', token_request)

        purchase = {
            'command': service_command_type,
            'access_code': access_code_id,
            'merchant_identifier': merchant_identifier_id,
            'merchant_reference': merchant_reference_val,
            'amount': amount_val,
            'currency': currency_val,
            'language': language_code,
            'customer_email': customer_email_val,
            'token_name': token_name_val,
            'customer_ip': customer_ip_addr,
            'signature': shasignature,
            'return_url': return_url_val
        }

        url = "https://sbpaymentservices.payfort.com/FortAPI/paymentApi"
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(purchase), headers=headers)
        print("response from amazon >>> ", r.json())
        response = r.json()
        url = response.get('3ds_url')
        return werkzeug.utils.redirect(url)

    @http.route('/payfort/response/message', type='http', auth="public", website=True, csrf=False, )
    def PayfortResponseMessage(self, **kw):
        print('test', kw)
        response_code_val = kw['response_code']
        print(response_code_val)
        if response_code_val == '14000':
            return request.render("iwesabe_website_theme.payfort_response_view")
        else:
            return request.render("iwesabe_website_theme.payfort_response_error")



    @http.route('/checkout/smsa', type='json', auth="public", website=True, csrf=False, )
    def CheckoutSmsa(self):
        order = request.website.sale_get_order()
        smsa = request.env['delivery.carrier'].sudo().search([('delivery_type', '=', 'smsa')])
        print("smsa", smsa.rate_shipment)
        vals = smsa.rate_shipment(order)
        print(vals)
        smsa_price = vals['price']
        order.write(({'carrier_price': smsa_price, 'carrier_id': smsa}))
        # order['carrier_price'] = smsa_price
        # print("s_p", order.read())
        values = {
            'smsa_cost': smsa_price,
            'website_sale_order': order
        }
        return values

    @http.route('/checkout/address', type='json', auth="public", website=True, csrf=False, )
    def CheckoutAddress(self):
        print("qwerty")

    @http.route('/shop/discount', type='json', auth="public", website=True, csrf=False,)
    def pricelist(self, promo):
        order = request.website.sale_get_order()
        coupon = request.env['sale.coupon.apply.code'].sudo().apply_coupon(order, promo)
        print("coupon", coupon)
        print("orderrrrrrrrrrrr", order.order_line)
        lines = order.order_line
        order.recompute_coupon_lines()
        print("orderlineeeeeeeeee", order.order_line)
        order.write(({'order_line': lines}))
        values = {
            'coupon_status': coupon
        }
        return values

    @http.route('/shop/rev/discount', type='json', auth="public", website=True, csrf=False,)
    def RevDiscount(self):
        order = request.website.sale_get_order()
        order_line = order.order_line
        print("llllllllll", order_line)
        flag = 1
        for lines in order_line:
            product = lines.product_id.filtered(lambda l: 'discount on total amount' in l.name)
            print("sssss", product)
            if product:
                print("gfffffffffffd")
                lines.unlink()
                flag = 2
        print("flag", flag)

        return flag





    @http.route(['/support'], type='http', auth="public", website=True)
    def InfiniarcSupport(self, **kw):
        value = {}
        value['type'] = request.env['terms.and.conditions'].sudo().search([])
        value['our_partners'] = request.env['our.partner'].sudo().search([('website_published', '=', True)])
        return request.render("iwesabe_website_theme.infiniarc_support", value)

    @http.route(['/page_render'], type="http", auth="public", website=True)
    def InfiniarcRender(self, **kw):
        print("Dynamic")
        order = request.website.sale_get_order()
        banks = request.env['company.banks'].sudo().search([])
        print('banks', banks.read())
        phone = order.company_id.mobile
        print("mobile", phone)
        values = {
            'order': order,
            'banks': banks,
            'mobile': phone
        }
        print(values)
        return request.render("iwesabe_website_theme.wire_response", values)

    @http.route(['/page_thanks'], type="json", auth="none")
    def InfiniarcThanks(self, active, **kw):
        print("static")
        print(active)

    @http.route(['/aboutus'], type='http', auth="public", website=True)
    def InfiniarcAboutUs(self, **kw):
        value = {}
        return request.render("iwesabe_website_theme.infiniarc_about_us_page", value)

    @http.route(['/terms-and-conditions'], type='http', auth="public", website=True)
    def InfiniarcTermsAndCondition(self, **kw):
        value = {}
        value['type'] = request.env['terms.and.conditions'].sudo().search([])
        value['terms'] = request.env['infiniarc.policy'].sudo().search([])
        return request.render("iwesabe_website_theme.infiniarc_terms_and_conditions", value)

    @http.route(['/terms/<model("terms.and.conditions"):conditions>'], type='http', auth="public", website=True)
    def TermsAndConditions(self, conditions, **post):
        print('conditions', conditions)
        value = {}
        value['type'] = request.env['terms.and.conditions'].sudo().search([])
        value['terms'] = request.env['infiniarc.policy'].sudo().search([('type', '=', conditions.types)])
        return request.render("iwesabe_website_theme.infiniarc_terms_and_conditions", value)

    @http.route(['/warranty/<model("warranty.warranty"):warranty>'], type='http', auth="public", website=True)
    def Warranty(self, warranty, **post):
        value = {}
        value['warranty'] = request.env['warranty.warranty'].sudo().search([])
        value['description'] = request.env['warranty.warranty'].sudo().search([('type', '=', warranty.type)])
        return request.render("iwesabe_website_theme.infiniarc_warranty", value)

    @http.route(['/warranty'], type='http', auth="public", website=True)
    def InfiniarcWarranty(self, **kw):
        value = {}
        value['warranty'] = request.env['warranty.warranty'].sudo().search([])
        value['description'] = request.env['warranty.warranty'].sudo().search([])
        return request.render("iwesabe_website_theme.infiniarc_warranty", value)

    @http.route(['/faq'], type='http', auth="public", website=True)
    def InfiniarcFaq(self, **kw):
        value = {}
        value['faq'] = request.env['faq.faq'].sudo().search([('type', '=', 'faq')])
        value['knowledge'] = request.env['faq.faq'].sudo().search([('type', '=', 'knowledge')])
        return request.render("iwesabe_website_theme.infiniarc_faq", value)

    @http.route(['/download'], type='http', auth="public", website=True)
    def InfiniarcDownload(self, **kw):
        value = {}
        value['driver'] = request.env['driver.download'].sudo().search([])
        return request.render("iwesabe_website_theme.infiniarc_download", value)

    @http.route(['/order_status'], type='http', auth="public", website=True)
    def InfiniarcOrderStatus(self, **kw):
        value = {}
        return request.render("iwesabe_website_theme.infiniarc_order_status", value)


    @http.route(['/contactus'], type='http', auth="public", website=True)
    def InfiniarcContactus(self, **kw):
        value = {}
        return request.render("iwesabe_website_theme.infiniarc_contactus_page", value)

    @http.route(['/order_history_status'], type='http', auth="public", website=True)
    def InfiniarcHistoryOrderStatus(self, **kw):
        value = {}
        value['sale_order'] = request.env['sale.order'].sudo().search([('name', '=', kw['Confirmation_number'])])
        return request.render("iwesabe_website_theme.order_history_status_page", value)

    @http.route(['/phone_number'], type='http', auth="public", website=True)
    def InfiniarcPhoneLogin(self, **kw):
        # digits = "0123456789"
        # OTP = ""
        # for i in range(6):
        #     OTP += digits[int(math.floor(random.random() * 10))]
        # new_user_id = request.request['user']
        # user = request.env['res.users'].sudo().browse(int(new_user_id))
        # otp_time = datetime.strptime(fields.Datetime.now(), DEFAULT_SERVER_DATETIME_FORMAT)
        # user.write({"otp": OTP, 'otp_time': otp_time})
        # user_partner = user.partner_id
        # template = request.env.ref("auth_signup_confirmation.otp_resend_email5")
        # if template:
        #     template.with_context(email_to=user_partner.email, otp=OTP).sudo().send_mail(res_id=user.id,
        #                                                                                  force_send=True)
        value = {}
        # value['sale_order'] = request.env['sale.order'].sudo().search([('name', '=', kw['Confirmation_number'])])
        return request.render("iwesabe_website_theme.phone_login_page", value)

    @http.route(['/otp_login'], type='http', auth="public", website=True)
    def InfiniarcOTPLogin(self, **kw):
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[int(math.floor(random.random() * 10))]
        partner_id = request.env['res.partner'].sudo().search([('phone', '=', kw.get('phone'))])
        for partner in partner_id:
            new_user_id = request.env['res.users'].sudo().search([('partner_id', '=', partner.id)])
            if not new_user_id:
                # return {'error': _('The Phone number you entered is not matching for any users')}
                raise ValidationError(_("The Phone number you entered is not matching for any users"))

            user = request.env['res.users'].sudo().browse(int(new_user_id))
            # otp_time = datetime.strptime(fields.Datetime.now(), DEFAULT_SERVER_DATETIME_FORMAT)
            otp_time = datetime.strptime(str(fields.Datetime.now()), DEFAULT_SERVER_DATETIME_FORMAT).date()
            # user.write({"otp": OTP, 'otp_time': otp_time})
        # user_partner = user.partner_id
        # template = request.env.ref("auth_signup_confirmation.otp_resend_email5")
        # if template:
        #     template.with_context(email_to=user_partner.email, otp=OTP).sudo().send_mail(res_id=user.id,
        #                                                                                  force_send=True)
        value = {}
        # value['sale_order'] = request.env['sale.order'].sudo().search([('name', '=', kw['Confirmation_number'])])
        return request.render("iwesabe_website_theme.otp_login_page", value)

    @http.route(['/shop/confirm-address'], type='http', auth="user", methods=['POST'], website=True)
    def ShopConfirmAddress(self, partner_id, **kw):
        if partner_id:
            partner_id = request.env['res.partner'].browse(int(partner_id))
            if partner_id:
                update_vals = {}
                if kw.get("first_name", False):
                    update_vals.update({
                        'name': kw.get("first_name", False)
                    })
                if kw.get("telephone", False):
                    update_vals.update({
                        'phone': kw.get("telephone", False)
                    })
                if kw.get("email", False):
                    update_vals.update({
                        'email': kw.get("email", False)
                    })
                if kw.get("street", False):
                    update_vals.update({
                        'street': kw.get("street", False)
                    })
                partner_id.write(update_vals)
        return request.redirect("/shop/payment")


class WebsiteSaleEcom(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super(WebsiteSaleEcom, self)._get_shop_payment_values(order, **kwargs)
        transaction_route = "/payment/transaction/custom"
        values['transaction_route'] = transaction_route

    @http.route(['/shop/checkout'], type='http', auth="public", website=True, sitemap=False)
    def checkout(self, **post):
        res = super(WebsiteSaleEcom, self).checkout(**post)
        order = request.website.sale_get_order()
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            return request.redirect('/web/login?redirect=/shop/confirm_order')
        return res

    def sitemap_shop(env, rule, qs):
        if not qs or qs.lower() in '/shop':
            yield {'loc': '/shop'}

        Category = env['product.public.category']
        dom = sitemap_qs2dom(qs, '/shop/category', Category._rec_name)
        dom += env['website'].get_current_website().website_domain()
        for cat in Category.search(dom):
            loc = '/shop/category/%s' % slug(cat)
            if not qs or qs.lower() in loc:
                yield {'loc': loc}

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=sitemap_shop)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        try:
            min_price = float(min_price)
        except ValueError:
            min_price = 0
        try:
            max_price = float(max_price)
        except ValueError:
            max_price = 0

        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list,
                        min_price=min_price, max_price=max_price, order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            company_currency = request.website.company_id.currency_id
            conversion_rate = request.env['res.currency']._get_conversion_rate(company_currency, pricelist.currency_id,
                                                                               request.website.company_id,
                                                                               fields.Date.today())
        else:
            conversion_rate = 1

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        options = {
            'displayDescription': True,
            'displayDetail': True,
            'displayExtraDetail': True,
            'displayExtraLink': True,
            'displayImage': True,
            'allowFuzzy': not post.get('noFuzzy'),
            'category': str(category.id) if category else None,
            'min_price': min_price / conversion_rate,
            'max_price': max_price / conversion_rate,
            'attrib_values': attrib_values,
            'display_currency': pricelist.currency_id,
        }
        # No limit because attributes are obtained from complete product list
        product_count, details, fuzzy_search_term = request.website._search_with_fuzzy("products_only", search,
                                                                                       limit=None,
                                                                                       order=self._get_search_order(
                                                                                           post), options=options)
        search_product = details[0].get('results', request.env['product.template']).with_context(bin_size=True)
        search_product = search_product.filtered(lambda product: product.is_published)
        product_count = len(search_product)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            # TODO Find an alternative way to obtain the domain through the search metadata.
            Product = request.env['product.template'].with_context(bin_size=True)
            domain = self._get_search_domain(search, category, attrib_values)

            # This is ~4 times more efficient than a search for the cheapest and most expensive products
            from_clause, where_clause, where_params = Product._where_calc(domain).get_sql()
            query = f"""
				SELECT COALESCE(MIN(list_price), 0) * {conversion_rate}, COALESCE(MAX(list_price), 0) * {conversion_rate}
				FROM {from_clause}
				WHERE {where_clause}
			"""
            request.env.cr.execute(query, where_params)
            available_min_price, available_max_price = request.env.cr.fetchone()

            if min_price or max_price:
                # The if/else condition in the min_price / max_price value assignment
                # tackles the case where we switch to a list of products with different
                # available min / max prices than the ones set in the previous page.
                # In order to have logical results and not yield empty product lists, the
                # price filter is set to their respective available prices when the specified
                # min exceeds the max, and / or the specified max is lower than the available min.
                if min_price:
                    min_price = min_price if min_price <= available_max_price else available_min_price
                    post['min_price'] = min_price
                if max_price:
                    max_price = max_price if max_price >= available_min_price else available_max_price
                    post['max_price'] = max_price

        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search(
                [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        offset = pager['offset']
        products = search_product[offset:offset + ppg]

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([
                ('product_tmpl_ids', 'in', search_product.ids),
                ('visibility', '=', 'visible'),
            ])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': fuzzy_search_term or search,
            'original_search': fuzzy_search_term and search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        }
        if filter_by_price_enabled:
            values['min_price'] = min_price or available_min_price
            values['max_price'] = max_price or available_max_price
            values['available_min_price'] = tools.float_round(available_min_price, 2)
            values['available_max_price'] = tools.float_round(available_max_price, 2)
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)

    @http.route([
        '''/products/ready-to-ship''',
        '''/products/ready-to-ship/page/<int:page>''',
    ], type='http', auth="public", website=True, sitemap=sitemap_shop)
    def shop_gear_store(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        try:
            min_price = float(min_price)
        except ValueError:
            min_price = 0
        try:
            max_price = float(max_price)
        except ValueError:
            max_price = 0

        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list,
                        min_price=min_price, max_price=max_price, order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            company_currency = request.website.company_id.currency_id
            conversion_rate = request.env['res.currency']._get_conversion_rate(company_currency, pricelist.currency_id,
                                                                               request.website.company_id,
                                                                               fields.Date.today())
        else:
            conversion_rate = 1

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        options = {
            'displayDescription': True,
            'displayDetail': True,
            'displayExtraDetail': True,
            'displayExtraLink': True,
            'displayImage': True,
            'allowFuzzy': not post.get('noFuzzy'),
            'category': str(category.id) if category else None,
            'min_price': min_price / conversion_rate,
            'max_price': max_price / conversion_rate,
            'attrib_values': attrib_values,
            'display_currency': pricelist.currency_id,
        }
        # No limit because attributes are obtained from complete product list
        product_count, details, fuzzy_search_term = request.website._search_with_fuzzy("products_only", search,
                                                                                       limit=None,
                                                                                       order=self._get_search_order(
                                                                                           post), options=options)
        search_product = details[0].get('results', request.env['product.template']).with_context(bin_size=True)
        search_product = search_product.filtered(
            lambda product: product.is_published and product.type_of_pc == 'normal')
        product_count = len(search_product)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            # TODO Find an alternative way to obtain the domain through the search metadata.
            Product = request.env['product.template'].with_context(bin_size=True)
            domain = self._get_search_domain(search, category, attrib_values)

            # This is ~4 times more efficient than a search for the cheapest and most expensive products
            from_clause, where_clause, where_params = Product._where_calc(domain).get_sql()
            query = f"""
				SELECT COALESCE(MIN(list_price), 0) * {conversion_rate}, COALESCE(MAX(list_price), 0) * {conversion_rate}
				FROM {from_clause}
				WHERE {where_clause}
			"""
            request.env.cr.execute(query, where_params)
            available_min_price, available_max_price = request.env.cr.fetchone()

            if min_price or max_price:
                # The if/else condition in the min_price / max_price value assignment
                # tackles the case where we switch to a list of products with different
                # available min / max prices than the ones set in the previous page.
                # In order to have logical results and not yield empty product lists, the
                # price filter is set to their respective available prices when the specified
                # min exceeds the max, and / or the specified max is lower than the available min.
                if min_price:
                    min_price = min_price if min_price <= available_max_price else available_min_price
                    post['min_price'] = min_price
                if max_price:
                    max_price = max_price if max_price >= available_min_price else available_max_price
                    post['max_price'] = max_price

        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search(
                [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        offset = pager['offset']
        products = search_product[offset:offset + ppg]

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([
                ('product_tmpl_ids', 'in', search_product.ids),
                ('visibility', '=', 'visible'),
            ])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': fuzzy_search_term or search,
            'original_search': fuzzy_search_term and search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        }
        if filter_by_price_enabled:
            values['min_price'] = min_price or available_min_price
            values['max_price'] = max_price or available_max_price
            values['available_min_price'] = tools.float_round(available_min_price, 2)
            values['available_max_price'] = tools.float_round(available_max_price, 2)
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)

        # my updates

    @http.route(['/get_dialogue_data'], type='json', auth='user',
                website=True)
    def get_dialogue_data(self, id, products, components, dict):
        dict_values = {}
        for k, v in dict.items():
            dict_values[int(k)] = int(dict[k])
        product_id = request.env['product.template'].browse(int(id))
        products = [int(x) for x in products]
        components_list = [int(x) for x in components]
        product_ids_list = product_id.component_lines.product_ids.filtered(
            lambda x: x.id in products)
        component_ids = product_id.component_lines.component_id.filtered(
            lambda x: x.id in components_list)
        parent_category_ids = product_id.component_lines.filtered(
            lambda x: x.component_id in component_ids).mapped(
            'parent_category_id')
        response = http.Response(
            template='iwesabe_website_theme.dialogue_box_content',
            qcontext={'product_ids_list': product_ids_list, 'product_id': product_id,
                      'component_ids': component_ids,
                      'categ_id': parent_category_ids,
                      'dict_values': dict_values})
        return response.render()

    @http.route(['/get_components_data'], type='json', auth='user',
                website=True)
    def get_components_data(self, id, type, main_product_id, d):
        product_id = request.env['product.product'].browse(int(id))
        product_main = request.env['product.template'].browse(int(main_product_id))
        if product_id:
            if type == 'cpu':
                if product_id.component_type == 'cpu':
                    values = {}
                    support_dict = {}
                    cpu_supported_boards = product_main.component_lines.product_ids.filtered(
                        lambda x: x.component_type == 'board' and x.cpu_support_id == product_id.cpu_type_id).ids
                    if (product_id.is_k_type):
                        cpu_supported_coolers = product_main.component_lines.product_ids.filtered(
                            lambda x: x.component_type == 'cooler' and x.type_cooler == 'air_cooler').ids

                    else:
                        cpu_supported_coolers = product_main.component_lines.product_ids.filtered(
                            lambda x: x.component_type == 'cooler' and x.type_cooler == 'water_cooler').ids
                    board_cpu_type = d.get('board_cpu_type')
                    board_supported_cpu = product_main.component_lines.product_ids.filtered(
                        lambda x: x.component_type == 'cpu' and x.cpu_type_id.id == int(board_cpu_type)).ids
                    if d.get('cooler_type') == 'air_cooler':
                        cooler_supported_cpu = product_main.component_lines.product_ids.filtered(
                            lambda x: x.component_type == 'cpu' and x.is_k_type).ids
                    elif d.get('cooler_type') == 'water_cooler':
                        cooler_supported_cpu = product_main.component_lines.product_ids.filtered(
                            lambda x: x.component_type == 'cpu' and not x.is_k_type).ids

                    support_dict['cooler_supported_cpu'] = cooler_supported_cpu
                    support_dict['cpu_supported_boards'] = cpu_supported_boards
                    support_dict['cpu_supported_coolers'] = cpu_supported_coolers
                    support_dict['board_supported_cpu'] = board_supported_cpu
                    values['type'] = product_id.cpu_type_id.id
                    values['oc'] = product_id.support_oc
                    values['k'] = product_id.is_k_type
                    values['supported_dict'] = support_dict
                    return values
            if type == 'board':
                if product_id.component_type == 'board':
                    values = {}
                    values['pc_support'] = product_id.cpu_support_id.id
                    values['mmry_support'] = product_id.memories_type_support_id.id
                    values['m2'] = product_id.m_2_support
                    values['series'] = product_id.serics_motherboard
                    return values
            if type == 'cooler':
                if product_id.component_type == 'cooler':
                    values = {}
                    values['cooler_type'] = product_id.type_cooler
                    if product_id.type_cooler != 'air_cooler':
                        values['cooler_air_height'] = ''
                    else:
                        values['cooler_air_height'] = product_id.air_height
                    values['cooler_radiator_size'] = product_id.radiator_size_id.id
                    values['cooler_fans_count'] = product_id.cooler_fans_count
                    return values
            if type == 'case':
                if product_id.component_type == 'case':
                    values = {}
                    values['case_type_cooler'] = product_id.type_cooler_support
                    if product_id.type_cooler_support == 'air_cooler' or product_id.type_cooler_support == 'both':
                        values['case_cooler_height'] = product_id.air_cooler_height
                    else:
                        values['case_cooler_height'] = ''
                    values['case_radiator_size_list'] = product_id.radiator_size_ids.ids
                    values['case_built_fans_no'] = product_id.built_fans_no
                    values['case_fans_support'] = product_id.fans_no_support
                    return values
            if type == 'memory':
                if product_id.component_type == 'memory':
                    values = {}
                    values['type'] = product_id.memories_type_id.id
                    return values
            if type == 'fans':
                if product_id.component_type == 'fans':
                    values = {}
                    values['fans_package_no'] = product_id.pak_fans_no
                    return values
            if type == 'm_2':
                if product_id.component_type == 'm_2':
                    values = {}
                    values['m_2_sum'] = product_id.m_2_no
                    return values

    @http.route(['/get_glowing_power_cards'], type='json', auth='user',
                website=True)
    def get_glowing_power_cards(self, sum, id, power_id, product_id):
        product_id = request.env['product.template'].browse(int(product_id))
        product_glow_list = product_id.component_lines.filtered(lambda x: x.component_id.id == int(power_id)).mapped(
            'product_ids').filtered(lambda x: x.power_value_support >= int(sum)).ids
        return product_glow_list

    # /my updates
    @http.route(['/get_refresh_template'], type='json', auth='user',
                website=True)
    def get_refresh_template(self, id):
        id = request.env['product.template'].browse(int(id))
        date_max = datetime.date.today() + relativedelta(
            days=id.max_delivery_days)
        date_min = datetime.date.today() + relativedelta(
            days=id.min_delivery_days)
        date_string_max = date_max.strftime('%d') + ' ' + date_max.strftime(
            '%b') + ', ' + date_max.strftime('%Y')
        date_string_min = date_min.strftime('%d') + ' ' + date_min.strftime(
            '%b') + ', ' + date_min.strftime('%Y')

        response = http.Response(
            template='iwesabe_website_theme.refresh_div',
            qcontext={'product_id': id, 'expected_date_min': date_string_min,
                      'expected_date_max': date_string_max})
        return response.render()

    @http.route(['/get_product_card_pop_up'], type='json', auth='user',
                website=True)
    def get_product_card_pop_up(self, id):
        product_id = request.env['product.product'].sudo().browse(
            int(id)).product_tmpl_id
        images = product_id.product_template_image_ids
        specs = {}
        specs[
            'Brand'] = product_id.brand_id.name if product_id.brand_id else None
        specs[
            'PC Type'] = product_id.filter_type.filter if product_id.filter_type else None
        spec_details = product_id.specification_line
        if spec_details:
            for rec in spec_details:
                specs[rec.item_id.name] = rec.name
        print(spec_details, 'd')
        specs[
            'Component Type'] = product_id.component_type if product_id.component_type else None
        if product_id.component_type == 'power':
            specs['Total Power Capacity'] = product_id.power_value_support
        else:
            specs['Power Watts'] = product_id.power_watt
        if product_id.component_type == 'cpu':
            specs[
                'CPU Type'] = product_id.cpu_type_id.name if product_id.cpu_type_id else None
            specs['Support OC'] = product_id.support_oc
            specs['Is K Type?'] = product_id.is_k_type
        if product_id.component_type == 'board':
            specs[
                'CPU Supported'] = product_id.cpu_support_id.name if product_id.cpu_support_id else None
            specs[
                'Memories Type Support'] = product_id.memories_type_support_id.name if product_id.memories_type_support_id else None
            specs[
                'Number of m.2 Support'] = product_id.m_2_support if product_id.m_2_support else 0
            specs['Series Mother-Board'] = product_id.serics_motherboard
        if product_id.component_type == 'cooler':
            if product_id.type_cooler == 'air_cooler':
                specs['Cooler Type'] = 'Air Cooler'
                specs[
                    'Height'] = product_id.air_height if product_id.air_height else 0
            elif product_id.type_cooler == 'water_cooler':
                specs['Cooler Type'] = 'Water Cooler'
            specs[
                'Radiator Size'] = product_id.radiator_size_id.name if product_id.radiator_size_id else None
            specs[
                'No. of fans'] = product_id.cooler_fans_count if product_id.cooler_fans_count else 0
        if product_id.component_type == 'case':
            if product_id.type_cooler_support in ['air_cooler', 'both']:
                if product_id.type_cooler_support == 'air_cooler':
                    specs['Type Cooler Support'] = 'Air Cooler'
                else:
                    specs['Type Cooler Support'] = 'Both(Air & Water)'
                specs[
                    'Air cooler Height support'] = product_id.air_cooler_height if product_id.air_cooler_height else 0
            elif product_id.type_cooler_support == 'Water Cooler':
                specs['Cooler Type'] = 'Water Cooler'
            specs['Radiator Size Values'] = product_id.radiator_size_ids.mapped(
                'name') if product_id.radiator_size_ids else None
            specs[
                'Built in fans No.'] = product_id.built_fans_no if product_id.built_fans_no else 0
            specs[
                'Fans Number Support'] = product_id.fans_no_support if product_id.fans_no_support else 0
        if product_id.component_type == 'memory':
            specs[
                'Memories Type'] = product_id.memories_type_id.name if product_id.memories_type_id else None
        if product_id.component_type == 'fans':
            specs['Package Fans No.'] = product_id.pak_fans_no
        if product_id.component_type == 'm_2':
            specs['No of M2.'] = product_id.m_2_no if product_id.m_2_no else 0

        response = http.Response(
            template='iwesabe_website_theme.dialogue_box_product_images',
            qcontext={'images': images, 'specs': specs})
        return response.render()

class InfiniarcPaymentPortal(payment_portal.PaymentPortal):
    @http.route(
        '/shop/payment/transaction/<int:order_id>', type='json', auth='public', website=True
    )
    def shop_payment_transaction(self, order_id, access_token, payment_option_id, **kwargs):
        """ Create a draft transaction and return its processing values.

        :param int order_id: The sales order to pay, as a `sale.order` id
        :param str access_token: The access token used to authenticate the request
        :param dict kwargs: Locally unused data passed to `_create_transaction`
        :return: The mandatory values for the processing of the transaction
        :rtype: dict
        :raise: ValidationError if the invoice id or the access token is invalid
        """
        # Check the order id and the access token
        print('or1', order_id)
        print('acce1', access_token)
        print("acff", payment_option_id)
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token)
        except MissingError as error:
            raise error
        except AccessError:
            raise ValidationError(_("The access token is invalid."))

        if order_sudo.state == "cancel":
            raise ValidationError(_("The order has been canceled."))
        print('kwa', kwargs)
        print('kcwa', [Command.set([order_id])])
        kwargs.update({
            'reference_prefix': None,  # Allow the reference to be computed based on the order
            'sale_order_id': order_id,  # Include the SO to allow Subscriptions to tokenize the tx
        })
        kwargs.pop('custom_create_values', None)  # Don't allow passing arbitrary create values
        print("=========================================", kwargs)
        # tx_sudo = self._create_transaction(
        #     custom_create_values={'sale_order_ids': [Command.set([order_id])]}, **kwargs,
        # )
        acquirer_sudo = request.env['payment.acquirer'].search([('provider', '=', "transfer")])
        # order = order_id
        order = request.website.sale_get_order()
        print("order1", order.read())
        company_id = order.company_id
        print("comp", company_id.name)
        amount = order.amount_total
        print("amoiut", amount)
        currency_id = company_id.currency_id.id
        print("curr", currency_id)
        partner_id = order.partner_id.id
        payment_option_id = payment_option_id.id
        flow = "direct"
        landing_route = "/shop/payment/validate"
        # tokenization_required_or_requested =
        tx_sudo = self._create_transaction(
            reference=order, amount=amount, currency_id=currency_id, partner_id=partner_id,
            payment_option_id=payment_option_id,
            flow=flow, tokenization_requested=False, landing_route=landing_route, **kwargs
        )
        print("tx_sudo", tx_sudo.read())
        # Store the new transaction into the transaction list and if there's an old one, we remove
        # it until the day the ecommerce supports multiple orders at the same time.
        last_tx_id = request.session.get('__website_sale_last_tx_id')
        print("last_id", last_tx_id)
        last_tx = request.env['payment.transaction'].browse(last_tx_id).sudo().exists()
        print("last", last_tx)
        if last_tx:
            PaymentPostProcessing.remove_transactions(last_tx)
        request.session['__website_sale_last_tx_id'] = tx_sudo.id
        print('ddd', tx_sudo._get_processing_values())
        return tx_sudo

    # def shop_payment_transaction(self, order_id, access_token, **kwargs):
    #     values = super(InfiniarcPaymentPortal, self).shop_payment_transaction(order_id,access_token,**kwargs)
    #     print(values)

    @http.route(["/payment/transaction/custom"], type="json", auth="public", website=True)
    def shop_payment_validate(self, active, transaction_id=None, sale_order_id=None, ):
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        print("fcb", active)
        if sale_order_id is None:
            order = request.website.sale_get_order()
            print('order1', order)
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            print('order2', order)
            assert order.id == request.session.get('sale_last_order_id')
        access_token = order._portal_ensure_token()
        payment_option_id = request.env['payment.acquirer'].search([('provider', '=', active)])
        print('opt', payment_option_id)
        transaction_id = self.shop_payment_transaction(order.id, access_token, payment_option_id)
        print('tra', transaction_id.reference)
        merchant_reference = transaction_id.reference
        provider = transaction_id.provider
        if transaction_id:
            tx = request.env['payment.transaction'].sudo().browse(transaction_id)
            print('tx', tx.id)
            print('order', order.read())
            assert tx.id in order.transaction_ids
            print("transact", order.transaction_ids)
        elif order:
            tx = order.get_portal_last_transaction()
            print('tx1', tx)
        else:
            tx = None

        if not order or (order.amount_total and not tx):
            print("shop@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            return request.redirect('/shop')

        if order:
            print("shop!@!@!@@!@!@!!!@!@!@!@!!!@!@!@!@!@!@!@!@!@!")
            order.with_context(send_email=True).action_confirm()

            print('tra', merchant_reference, type(merchant_reference), '>>>>>>>')
            return {
                'merchant_reference': merchant_reference,
                'provider': provider
            }

            # clean context and session, then redirect to the confirmation page
        request.website.sale_reset()
        # if tx.id and tx.state == 'draft':
        #     return request.redirect('/shop')

        PaymentPostProcessing.remove_transactions(tx)
        return {
            'merchant_reference': merchant_reference
        }
