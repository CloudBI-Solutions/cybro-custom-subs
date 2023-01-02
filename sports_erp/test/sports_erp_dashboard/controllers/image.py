import base64
import json

from odoo.addons.http_routing.models.ir_http import slug
from odoo import fields, _
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager
from collections import OrderedDict
from odoo.http import request, route
from odoo.addons.base.models.res_partner import _tz_get
from datetime import datetime, date
from odoo.addons.website_sale.controllers.main import WebsiteSale
from dateutil.relativedelta import relativedelta
import pytz


class ImagePortal(CustomerPortal):

    @route(['/update/image_template'],
           type='http', auth="user", website=True)
    def update_image(self, **post):
        print(post, "post")
        keys = []
        values = []
        length = len(post)
        print(length, "length")
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        print(organisation)
        index = max(map(lambda k: k.split('_')[1], post.keys()))
        minimum = min(map(lambda k: k.split('_')[1], post.keys()))
        # request.env['home.image'].sudo().search([]).unlink()
        # print(request.env['home.image'].sudo().search([]))
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
                print(image, "image")
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
            print(post.get('name_'+str(i)))
            print(post.get('description_'+str(i)))
        return request.redirect('/my/edit_home_image')

    @route(['/update/gallery/images'],
           type='http', auth="user", website=True)
    def update_gallery_image(self, **post):
        keys = []
        values = []
        length = len(post)
        print(post, "length")
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        print(organisation)
        index = max(map(lambda k: k.split('_')[1], post.keys()))
        minimum = min(map(lambda k: k.split('_')[1], post.keys()))
        # request.env['home.image'].sudo().search([]).unlink()
        # print(request.env['home.image'].sudo().search([]))
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

            print(post.get('description_' + str(i)))
        return request.redirect('/my/edit_gallery_image')
