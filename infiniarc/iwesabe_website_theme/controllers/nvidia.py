# from werkzeug.exceptions import NotFound
from odoo import http, models, tools, fields, _
from odoo.http import Controller, request, route, content_disposition
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class InfiniarcNvidia(http.Controller):

    @http.route(['/nvidia'], type='http', auth="public", website=True)
    def Infiniarc_nvidia(self, **post):
        values = {}
        domain = [('is_published', '=', True)]
        micro = request.env['featured.product'].sudo().search([], limit=4)
        featured = micro.featured_product_ids.featured_product
        values['featured'] = []
        for feature in featured:
            if feature.is_published == True:
                values['featured'] += feature
        single = micro.single_ids.single_product
        values['single'] = []
        for singl in single:
            if singl.is_published == True:
                values['single'] += singl

        values['banner'] = request.env['micro.dynamic.deals.banner'].sudo().search([('show', '=', True)])

        return request.render("iwesabe_website_theme.infiniarc_nvidia_page", values)

    @http.route(['/quick/model'], type='json', auth='public', website=True)
    def ProductsQuickView(self, **post):
        values = {}
        product = request.env['product.template'].sudo().browse(int(post.get('id')))
        print('produc//...t', product, product.name, product.price)

        response = http.Response(
            template='iwesabe_website_theme.modal_dialogue_quick_view',
            qcontext={'product_id': product})
        return response.render()

    @http.route(['/microdynamic'], type='json', auth='public', website=True)
    def MicroDynamicView(self, **post):
        values = {}
        print('postmicro', post)
        product = request.env['product.template'].sudo().browse(int(post.get('id')))
        print('micro product', product)

        response = http.Response(
            template='iwesabe_website_theme.modal_dialogue_micro_view',
            qcontext={'product': product})
        return response.render()

    @http.route(['/gear/model'], type='json', auth='public', website=True)
    def ProductsGearView(self, **post):
        values = {}
        product = request.env['product.template'].sudo().browse(int(post.get('id')))

        response = http.Response(
            template='iwesabe_website_theme.modal_dialogue_gear_view',
            qcontext={'product': product})
        return response.render()

    @http.route(['/special/model'], type='json', auth='public', website=True)
    def ProductsSpecialView(self, **post):
        values = {}
        product = request.env['product.template'].sudo().browse(int(post.get('id')))

        response = http.Response(
            template='iwesabe_website_theme.modal_dialogue_special_view',
            qcontext={'product': product})
        return response.render()

    @http.route(['/pc/model'], type='json', auth='public', website=True)
    def ProductsPCView(self, **post):
        values = {}
        product = request.env['product.template'].sudo().browse(int(post.get('id')))
        response = http.Response(
            template='iwesabe_website_theme.modal_dialogue_pc_view',
            qcontext={'product': product})
        return response.render()

    # aswathi
    @http.route(['/product/spec_model'], type='json', auth='public', website=True)
    def ProductsSpecificationView(self, **post):
        values = {}
        product = request.env['product.template'].sudo().browse(int(post.get('id')))
        component_type_parent = request.env['component.parents.type'].sudo().search([])
        print('component_type_parent', component_type_parent)
        response = http.Response(
            template='iwesabe_website_theme.modal_dialogue_product_spec',
            qcontext={'product': product,
                      'component_type_parent': component_type_parent})
        return response.render()

    @http.route(['/products/desktops'], type='http', auth='public', website=True)
    def ProductDesktopView(self, **post):
        return request.redirect('/', 303)
