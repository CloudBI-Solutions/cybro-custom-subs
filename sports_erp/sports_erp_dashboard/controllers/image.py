import base64
import json

from odoo.addons.http_routing.models.ir_http import slug
from odoo import fields, _
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager
from collections import OrderedDict
from odoo.http import request, route


class ImagePortal(CustomerPortal):

    @route(['/update/image_template'],
           type='http', auth="user", website=True)
    def update_image(self, **post):
        if post:
            org_domain = []
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
            if request.httprequest.cookies.get('select_organisation') is not None:
                org_domain.append(('id', '=',
                                   request.httprequest.cookies.get(
                                       'select_organisation')))
            organisation = request.env['organisation.organisation'].sudo().search(
                org_domain, limit=1)
            index = max(map(lambda k: k.split('_')[1], post.keys()))
            minimum = min(map(lambda k: k.split('_')[1], post.keys()))
            for i in range(int(minimum),int(index)+1):
                print(post.get('id_' + str(i)), "kkkk")
                if post.get('id_' + str(i)):
                    values = {}
                    image = request.env['home.image'].sudo().browse(int(post.get('id_' + str(i))))
                    values = {
                        'name': post.get('name_' + str(i)),
                        'description': post.get('description_' + str(i)),
                        'company_id': request.env.user.company_id.id,
                        'organisation_ids': [(4, int(organisation))]
                    }
                    if post.get('image_' + str(i)):
                        print(post.get('image_' + str(i)), )
                        values['image'] = base64.b64encode(
                                post.get('image_' + str(i)).read()) if post.get(
                                'image_' + str(i)) else False
                    image.sudo().write(values)
                else:
                    if post.get('image_' + str(i)):
                        request.env['home.image'].sudo().create({
                            'name': post.get('name_'+str(i)),
                            'description': post.get('description_'+str(i)),
                            'image': base64.b64encode(
                                post.get('image_'+str(i)).read()) if post.get('image_'+str(i)) else False,
                            'company_id': request.env.user.company_id.id,
                            'organisation_ids': [(4, int(organisation))]
                        })
        return request.redirect('/my/edit_home_image')

    @route(['/remove/home/image'],
           type='http', auth="user", website=True)
    def remove_image(self, **post):
        image = request.env['home.image'].sudo().browse(
            int(post.get('image')))
        if image:
            image.sudo().unlink()
        return request.redirect('/my/edit_home_image')

    @route(['/update/gallery/images'],
           type='http', auth="user", website=True)
    def update_gallery_image(self, **post):
        if post:
            org_domain = []
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
            if request.httprequest.cookies.get('select_organisation') is not None:
                org_domain.append(('id', '=',
                                   request.httprequest.cookies.get(
                                       'select_organisation')))
            organisation = request.env['organisation.organisation'].sudo().search(
                org_domain, limit=1)
            index = max(map(lambda k: k.split('_')[1], post.keys()))
            minimum = min(map(lambda k: k.split('_')[1], post.keys()))
            for i in range(int(minimum), int(index) + 1):
                if post.get('image_' + str(i)):
                    request.env['home.gallery'].sudo().create({
                        'name': post.get('name_' + str(i)),
                        'image': base64.b64encode(
                            post.get('image_' + str(i)).read()) if post.get(
                            'image_' + str(i)) else False,
                        'company_id': request.env.user.company_id.id,
                        'organisation_ids': [(4, int(organisation))]
                    })
        return request.redirect('/my/edit_gallery_image')

    @route(['/remove/gallery/image'],
           type='http', auth="user", website=True)
    def gallery_image(self, **post):
        image = request.env['home.gallery'].sudo().browse(
            int(post.get('image')))
        if image:
            image.sudo().unlink()
        return request.redirect('/my/edit_gallery_image')
