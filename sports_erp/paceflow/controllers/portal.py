
import base64

from odoo.addons.http_routing.models.ir_http import slug
from werkzeug.exceptions import Forbidden
from odoo import fields
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request, route
from datetime import datetime
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSalePaceflowClient(WebsiteSale):
    @http.route([
        '/shop/confirmation',
    ], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        response = super(WebsiteSalePaceflowClient,
                         self).shop_payment_confirmation(**post)
        order_lines = response.qcontext['order'].order_line
        if request.env.context.get('uid'):
            paceflow_product = request.env['product.product'].sudo().browse(
                               request.env.ref('paceflow.paceflow_package').id)
            for line in order_lines:
                if line.product_id == paceflow_product:
                    partner = request.env.user.partner_id
                    client = request.env['paceflow.client'].sudo().search(
                        [('partner_id', '=', partner.id)])
                    partner.sudo().write({
                        'is_client': True,
                    })
                    if not client:
                        request.env['paceflow.client'].sudo().create(
                            {
                                'partner_id': partner.id,
                            })
            return response


class Portal(CustomerPortal):

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        client = request.env['paceflow.client'].sudo().search(
                [('partner_id', '=', partner.id)])
        # child_contacts = client.child_ids
        if partner.is_client:
            params = request.env['ir.config_parameter'].sudo()
            mobile = params.get_param('paceflow.mobile')
            tablet = params.get_param('paceflow.tablet')
            desktop = params.get_param('paceflow.desktop')
            values.update({
                'mobile': mobile,
                'tablet': tablet,
                'desktop': desktop,
            })
            if client:
                child_contacts = client.child_ids
                values.update({
                    'child_contacts': child_contacts,
                })
            else:
                values.update({
                    'child_contacts': '',
                })
            response = request.render("paceflow.paceflow_portal_my_home", values)
            return response
        return request.render("portal.portal_my_home", values)

    # ( UPLOAD PAGE LOAD)
    @route(['/my/upload'], type='http', auth='user', website=True)
    def upload_form(self, **kw):
        if not kw:
            return request.redirect("/my/")
        else:
            child_id = request.env['paceflow.child'].browse(
                int(kw.get('child_id')))
            values = {}
            partner = request.env.user.partner_id
            request.env.cr.execute(
                """ SELECT id FROM 
                    paceflow_client WHERE
                    partner_id = %s """, [partner.id])
            client_id = request.env.cr.dictfetchall()
            client = request.env['paceflow.client'].sudo().browse(
                        client_id[0]['id'])
            child_contacts = client.child_ids
            values.update({
                'child_id': child_id,
                'partner': partner,
                'child_contacts': child_contacts,
            })
            response = request.render("paceflow.upload_rear_video_form", values)
            response.headers['X-Frame-Options'] = 'DENY'
            return response

    #REAR VIDEO SUBMIT
    @route(['/my/video_submit'], type='http', auth='user', website=True)
    def rear_video_submit(self, **post):
        if not post:
            return request.redirect("/my/")
        else:
            print("post", post)
            partner = request.env.user.partner_id
            coach = request.env['paceflow.client'].sudo().search([
                ('partner_id', '=', partner.id)
            ])
            child = request.env['paceflow.child'].sudo().browse(
                                int(post['upload_child_id']))
            if post:
                assessment = request.env['assessment.assessment'].sudo().create({
                    'partner_id': coach.id,
                    'child_id': child.id,
                    'highest_standard': child.highest_standard,
                    'hand': child.partner_id.hand,
                    'dob': child.dob,
                    'report_date': fields.Date.today(),
                    'name': '%s - %s' % (child.partner_id.name,
                                         fields.Date.today()),
                })
                attachments = request.env['ir.attachment']
                if post.get('attachment_rear'):
                    attachment_rear = attachments.sudo().create({
                        'name': post.get('attachment_rear').filename,
                        'type': 'binary',
                        'datas': base64.b64encode(post.get('attachment_rear').read()),
                        'res_model': assessment._name,
                        'res_id': assessment.id,
                        'reference': post.get('reference'),
                        'upload_date': post.get('date'),
                    })
                    assessment.sudo().write({
                        'attachment_ids': [(4, attachment_rear.id)],
                        'rear_video': attachment_rear.datas,
                        'rear_reference': post.get('reference')
                    })
                elif post.get('record_rear'):
                    attachment_rear = attachments.sudo().create({
                        'name': post.get('record_rear').filename,
                        'type': 'binary',
                        'datas': base64.b64encode(post.get('record_rear').read()),
                        'res_model': assessment._name,
                        'res_id': assessment.id,
                        'reference': post.get('reference'),
                        'upload_date': post.get('date'),
                    })
                    assessment.sudo().write({
                        'attachment_ids': [(4, attachment_rear.id)],
                        'rear_video': attachment_rear.datas,
                        'rear_reference': post.get('reference')
                    })
                values = {}
                if assessment:
                    values.update({
                        'child_id': child,
                        'assessment_id': assessment
                    })
                    response = request.render(
                        "paceflow.upload_side_video_form", values)
                else:
                    response = request.render("paceflow.portal_upload_error_page")
                response.headers['X-Frame-Options'] = 'DENY'
                return response

    #SIDE VIDEO SUBMIT
    @route(['/my/upload_complete'], type='http', auth='user', website=True)
    def side_video_submit(self, **post):
        if post:
            assessment = request.env['assessment.assessment'].sudo().browse(
                int(post.get('assessment_id_video'))
            )
            attachments = request.env['ir.attachment']
            if post.get('attachment_side'):
                attachment_side = attachments.sudo().create({
                    'name': post.get('attachment_side').filename,
                    'type': 'binary',
                    'datas': base64.b64encode(post.get('attachment_side').read()),
                    'res_model': assessment._name,
                    'res_id': assessment.id,
                    'reference': post.get('reference'),
                    'upload_date': post.get('date'),
                })
                assessment.sudo().write({
                    'attachment_ids': [(4, attachment_side.id)],
                    'side_video': attachment_side.datas,
                    'side_reference': post.get('reference')
                })
            elif post.get('record_side'):
                attachment_side = attachments.sudo().create({
                    'name': post.get('record_side').filename,
                    'type': 'binary',
                    'datas': base64.b64encode(
                        post.get('record_side').read()),
                    'res_model': assessment._name,
                    'res_id': assessment.id,
                    'reference': post.get('reference'),
                    'upload_date': post.get('date'),
                })
                assessment.sudo().write({
                    'attachment_ids': [(4, attachment_side.id)],
                    'side_video': attachment_side.datas,
                    'side_reference': post.get('reference')
                })
            if assessment:
                response = request.render(
                    "paceflow.portal_upload_thanks_page")
            else:
                response = request.render("paceflow.portal_upload_error_page")

            response.headers['X-Frame-Options'] = 'DENY'
            return response

    @route(['/my/dashboard'], type='http', auth='user', website=True)
    def client_dashboard(self):
        values = {}
        partner = request.env.user.partner_id
        request.env.cr.execute(
            """ SELECT id FROM 
                paceflow_client WHERE
                partner_id = %s """, [partner.id])
        client_id = request.env.cr.dictfetchall()
        client = request.env['paceflow.client'].sudo().browse(
            client_id[0]['id'])
        child_contacts = client.child_ids
        values.update({
            'child_contacts': child_contacts,
        })
        response = request.render("paceflow.child_contact_list", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/profile'], type='http', auth='user', website=True)
    def profile(self):
        values = {}
        partner = request.env.user.partner_id
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        values.update({
            'partner': partner,
            'states': states,
            'countries': countries,
        })
        code = partner.phone.split(" ")
        if len(code) > 1:
            values.update({
                'country_code': code[0],
                'number': code[1],
            })
        else:
            values.update({
                'country_code': '',
                'number': code[0],
            })
        response = request.render("paceflow.my_profile", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    #UPDATE PROFILE
    @route(['/my/update_profile'], type='http', auth='user', website=True)
    def update_profile(self, **post):
        print('***', post)
        partner = request.env['res.partner'].browse(
                                        int(post['partner']))
        partner_name = post.get('partner_name').rpartition(" ")
        partner_first = partner_name[0]
        partner_last = partner_name[-1]
        if not partner_first:
            partner_first = partner_name[-1]
            partner_last = ''
        values = {
            'name': partner_first,
            'last_name': partner_last,
            'email': post.get('email'),
            'phone': post.get('code') + ' ' + post.get('phone'),
            'street': post.get('house'),
            'street2': post.get('street'),
            'city': post.get('town'),
            'state_id': int(post.get('state_id')),
            'zip': post.get('phonecode'),
            'country_id': int(post.get('country_id')),
        }
        if post.get('photo'):
            values.update({
                'image_1920': base64.b64encode(post.get('photo').read())
            })
        partner.sudo().write(values)
        return request.redirect("/my/profile")

    @route(['/my/history_dashboard'], type='http', auth='user', website=True)
    def client_history_dashboard(self):
        values = {}
        partner = request.env.user.partner_id
        request.env.cr.execute(
            """ SELECT id FROM 
                paceflow_client WHERE
                partner_id = %s """, [partner.id])
        client_id = request.env.cr.dictfetchall()
        client = request.env['paceflow.client'].sudo().browse(
            client_id[0]['id'])
        child_contacts = client.child_ids
        values.update({
            'child_contacts': child_contacts,
        })
        response = request.render("paceflow.history_child_list", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/history_dashboard/<int:child_id>',
            '/history_dashboard/<int:child_id>'],
           type='http', auth='user',
           website=True)
    def history_dashboard(self, child_id=None):
        child = request.env['paceflow.child'].sudo().browse(int(child_id))
        child_partner = child.partner_id
        partner = request.env.user.partner_id
        request.env.cr.execute(
            """ SELECT id FROM 
                paceflow_client WHERE
                partner_id = %s """, [partner.id])
        client_id = request.env.cr.dictfetchall()
        client = request.env['paceflow.client'].sudo().browse(
            client_id[0]['id'])
        client_children = client.child_ids
        if child.id not in client_children.mapped('id'):
            return Forbidden()
        values = {}
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)
        request.env.cr.execute(
            """ SELECT id FROM 
                assessment_assessment WHERE
                child_id = %s AND stage_id = %s
                ORDER BY done_date ASC
                LIMIT 10 """, [child_partner.id, stage.id])
        assessments_id = [assessment_id['id']
                          for assessment_id in request.env.cr.dictfetchall()]
        assessments = request.env['assessment.assessment'].sudo().browse(
                                                            assessments_id)
        assessment = assessments[0]
        values.update({
            'child': child_partner,
            'assessment': assessment,
            'assessments': assessments
        })
        response = request.render("paceflow.portal_history_dashboard", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    # CHILD DETAILS/ ASSESSMENT REPORT

    @route(['/my/assessment_report/<int:child_id>', '/assessment_report/<int:child_id>'],
           type='http', auth='user', website=True)
    def assessment_report(self, child_id=None):
        if request.env.user.partner_id.is_client:
            partner = request.env.user.partner_id
            child = request.env['paceflow.child'].sudo().browse(int(child_id))
            print("child", child)
            child_partner = child.partner_id
            client = request.env['paceflow.client'].sudo().search([
                ('partner_id', '=', partner.id)])
            print("client", client)
            client_children = client.child_ids
            if child.id not in client_children.mapped('id'):
                return Forbidden()
            values = {}
            stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)
            assessments = request.env['assessment.assessment'].sudo().search(
                [('stage_id', '=', stage.id), ('child_id', '=', child.id)],
                order='report_date desc')
            assessment = request.env['assessment.assessment'].sudo().search(
                [('stage_id', '=', stage.id), ('child_id', '=', child.id)],
                order='report_date desc', limit=1)

            values.update({
                'partner': partner,
                'child': child,
                'child_partner': child_partner,
                'assessments': assessments,
                'assessment': assessment,
                'img_summary1': assessment.img_summary_overall_1,
                'img_summary2': assessment.img_summary_overall_2,
            })
            print("child", child.id)
            response = request.render("paceflow.portal_client_dashboard", values)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        elif request.env.user.partner_id.is_parent:
            parent = request.env.user.partner_id
            child = request.env['paceflow.child'].sudo().browse(int(child_id))
            child_partner = child.partner_id
            values = {}
            stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)
            assessments = request.env['assessment.assessment'].sudo().search(
                [('stage_id', '=', stage.id), ('child_id', '=', child.id)],
                order='report_date desc')
            assessment = request.env['assessment.assessment'].sudo().search(
                [('stage_id', '=', stage.id), ('child_id', '=', child.id)],
                order='report_date desc', limit=1)
            values.update({
                'partner': parent,
                'child': child,
                'child_partner': child_partner,
                'assessments': assessments,
                'assessment': assessment,
                'img_summary1': assessment.img_summary_overall_1,
                'img_summary2': assessment.img_summary_overall_2,
            })
            print("child", child.id)
            response = request.render("paceflow.portal_client_dashboard",
                                      values)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        else:
            return Forbidden()

    # PLAYER LEGALITY
    @route(['/my/assessment_report/<int:child_id>/legality/<int:assessment_id>',
            '/child_details/<int:child_id>/legality/<int:assessment_id>'],
           type='http', auth='user', website=True)
    def legality(self, **kwargs):
        values = {}
        child = request.env['paceflow.child'].sudo().browse(
                                            int(kwargs['child_id']))
        assessment = request.env['assessment.assessment'].sudo().browse(
                                            int(kwargs['assessment_id']))
        values.update({
            'child': child,
            'assessment': assessment,
        })
        if assessment.legality_note_ids:
            values.update({
                'legality_comments': assessment.legality_note_ids
            })
        print("values", values)
        response = request.render("paceflow.legality_dashboard", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    #PLAYER STABILITY
    @route(['/my/assessment_report/<int:child_id>/stability/<int:assessment_id>',
            '/child_details/<int:child_id>/stability/<int:assessment_id>'],
           type='http', auth='user', website=True)
    def stability(self, **kwargs):
        values = {}
        child = request.env['paceflow.child'].sudo().browse(
            int(kwargs['child_id']))
        assessment = request.env['assessment.assessment'].sudo().browse(
            int(kwargs['assessment_id']))
        values.update({
            'child': child,
            'assessment': assessment
        })
        if assessment.stability_note_ids:
            values.update({
                'stability_comments': assessment.stability_note_ids
            })
        response = request.render("paceflow.stability_dashboard", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    # PLAYER MOMENTUM

    @route(['/my/assessment_report/<int:child_id>/momentum/<int:assessment_id>',
         '/child_details/<int:child_id>/momentum/<int:assessment_id>'],
        type='http', auth='user', website=True)
    def momentum(self, **kwargs):
        values = {}
        child = request.env['paceflow.child'].sudo().browse(
            int(kwargs['child_id']))
        assessment = request.env['assessment.assessment'].sudo().browse(
            int(kwargs['assessment_id']))
        values.update({
            'child': child,
            'assessment': assessment
        })
        if assessment.momentum_note_ids:
            values.update({
                'momentum_comments': assessment.momentum_note_ids
            })
        print("momentum", values)
        response = request.render("paceflow.momentum_dashboard", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response\

    # PLAYER PACEFLOW

    @route(['/my/assessment_report/<int:child_id>/paceflow/<int:assessment_id>',
         '/child_details/<int:child_id>/paceflow/<int:assessment_id>'],
        type='http', auth='user', website=True)
    def pacelfow(self, **kwargs):
        values = {}
        child = request.env['paceflow.child'].sudo().browse(
            int(kwargs['child_id']))
        assessment = request.env['assessment.assessment'].sudo().browse(
            int(kwargs['assessment_id']))
        values.update({
            'child': child,
            'assessment': assessment
        })
        if assessment.paceflow_note_ids:
            values.update({
                'paceflow_comments': assessment.paceflow_note_ids
            })
        response = request.render("paceflow.paceflow_dashboard", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    # EDIT CHILD

    @route(['/my/edit_child/<int:child_id>'], type='http', auth='user', website=True)
    def edit_child(self, **kwargs):
        if request.env.user.partner_id.is_client:
            values = {}
            child = request.env['paceflow.child'].sudo().browse(
                                            int(kwargs['child_id']))
            partner = request.env.user.partner_id
            child_partner = child.partner_id
            request.env.cr.execute(
                """ SELECT id FROM 
                    paceflow_client WHERE
                    partner_id = %s """, [partner.id])
            client_id = request.env.cr.dictfetchall()
            client = request.env['paceflow.client'].sudo().browse(
                client_id[0]['id'])
            client_children = client.child_ids
            if child.id not in client_children.mapped('id'):
                return Forbidden()
            values.update({
                'partner': partner,
                'child_partner': child_partner,
                'child': child,
            })
            code = child.phone.split(" ")
            if len(code) > 1:
                values.update({
                    'country_code': code[0],
                    'number': code[1],
                })
            else:
                values.update({
                    'country_code': '',
                    'number': code[0],
                })
            child_group_ids = child.group_ids
            groups = request.env['paceflow.child.group'].search([
                ('id', 'not in', child_group_ids.ids)])
            child_parent_ids = child.parent_ids
            parents = request.env['paceflow.parents'].search([
                ('id', 'not in', child_parent_ids.ids)
            ])
            values.update({
                'child_groups': child_group_ids,
                'groups': groups,
                'child_parents': child_parent_ids,
                'parents': parents,
                'client_view': True,
                'parent_view': False
            })
            response = request.render(
                "paceflow.child_edit_form_template", values)
            response.headers['X-Frame-Options'] = 'DENY'
            return response

        elif request.env.user.partner_id.is_parent:
            print("haii")
            values = {}
            child = request.env['paceflow.child'].sudo().browse(
                int(kwargs['child_id']))
            child_partner = child.partner_id
            parent = request.env.user.partner_id
            values.update({
                'partner': parent,
                'child_partner': child_partner,
                'child': child,
            })
            code = child.phone.split(" ")
            if len(code) > 1:
                values.update({
                    'country_code': code[0],
                    'number': code[1],
                })
            else:
                values.update({
                    'country_code': '',
                    'number': code[0],
                })
            child_group_ids = child.group_ids
            groups = request.env['paceflow.child.group'].search([
                ('id', 'not in', child_group_ids.ids)])
            values.update({
                'child_groups': child_group_ids,
                'groups': groups,
                'client_view': False,
                'parent_view': True
            })
            response = request.render(
                "paceflow.child_edit_form_template", values)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        else:
            return Forbidden()

    # UPLOAD VIDEO FROM CHILD VIEW

    @route(['/my/upload/<int:child_id>'], type='http', auth='user',
           website=True)
    def upload_video_child(self, **kwargs):
        child_id = request.env['paceflow.child'].browse(int(kwargs.get('child_id')))
        values = {}
        partner = request.env.user.partner_id
        request.env.cr.execute(
            """ SELECT id FROM 
                paceflow_client WHERE
                partner_id = %s """, [partner.id])
        client_id = request.env.cr.dictfetchall()
        client = request.env['paceflow.client'].sudo().browse(
            client_id[0]['id'])
        child_contacts = client.child_ids
        values.update({
            'child_id': child_id,
            'partner': partner,
            'child_contacts': child_contacts,
        })
        response = request.render(
            "paceflow.portal_upload_form", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    # GROUPSSSSSS>>>>>>

#GROUP HOME>>>>>>
    @route(['/my/group'], type='http', auth='user', website=True)
    def my_group(self, **post):
        values = {}
        partner = request.env.user.partner_id
        coach = request.env['paceflow.client'].search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        groups = request.env['paceflow.child.group'].search([
            ('responsible_user', '=', coach.id)
        ])
        values.update({
            'groups': groups,
        })
        response = request.render("paceflow.group_home", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    #ADD NEW GROUP/  Group Create
    @route(['/my/create_group'], type='http', auth='user', website=True)
    def group_create(self, **post):
        players = request.env['paceflow.child'].search([])
        response = request.render("paceflow.group_create", {'players': players})
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    #GROUP submit
    @route(['/my/submit_group'], type='http', auth='user', website=True)
    def group_submit(self, **post):
        child_ids = list(map(int, request.httprequest.form.getlist('childs')))
        coach = request.env['paceflow.client'].search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        group = request.env['paceflow.child.group'].sudo().create({
            'name': post.get('group-name'),
            'description': post.get('group-description'),
            'responsible_user': coach.id
        })
        if post.get('photo'):
            group.write({
                'image_1920': base64.b64encode(post.get('photo').read()),
            })
        if child_ids:
            for child_id in child_ids:
                group.write({
                    'child_ids': [(4, child_id)]
                })
        coach.sudo().write({
            'group_ids': [(4, group.id)]
        })
        return request.redirect("/my/group")

    #GROUP VIEW>>>>>>
    @route(['/my/group_details/<int:group_id>'], type='http',
           auth='user', website=True)
    def group_details(self, **kwargs):
        group = request.env['paceflow.child.group'].browse(
            int(kwargs.get('group_id')))
        values = {}
        values.update({
            'group': group})
        group_players = group.child_ids
        values.update({
            'group_players': group_players,
        })
        response = request.render("paceflow.group_view",
                                  values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    #GROUP EDIT>>>>>>>
    @route(['/my/group_edit/<int:group_id>'], type='http',
           auth='user', website=True)
    def group_edit(self, **kwargs):
        group = request.env['paceflow.child.group'].browse(
            int(kwargs.get('group_id')))
        values = {}
        values.update({
            'group': group})
        group_players = group.child_ids
        players = request.env['paceflow.child'].search([
            ('id', 'not in', group_players.ids)
        ])
        values.update({
            'group_players': group_players,
            'players': players
        })
        response = request.render("paceflow.group_edit",
                                  values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    #GROUP UPDATE
    @route(['/my/update_group'], type='http', auth='user', website=True)
    def group_update(self, **post):
        group = request.env['paceflow.child.group'].browse(
                                                        int(post.get('id')))
        child_ids = list(map(int, request.httprequest.form.getlist('childs')))
        group.write({
            'name': post.get('group_name'),
            'description': post.get('description'),
        })
        group.write({
            'child_ids': [(5, 0, 0)]
        })
        if post.get('photo'):
            group.write({
                'image_1920': base64.b64encode(post.get('photo').read()),
            })
        if child_ids:
            for child_id in child_ids:
                group.write({
                    'child_ids': [(4, child_id)]
                })
        return request.redirect("/my/group_details/%s" % group.id)

    # PARENT TEMPLATES>>>>>>

#Parent HOME >>>
    @route(['/my/parent_home'], type='http', auth='user', website=True)
    def parent_home(self):
        parents = request.env['paceflow.parents'].search([])
        response = request.render("paceflow.parent_home", {'parent_contacts': parents})
        response.headers['X-Frame-Options'] = 'DENY'
        return response

#Parent Creation >>>

    @route(['/my/create_parent'], type='http', auth='user', website=True)
    def create_parent(self):
        childs = request.env['paceflow.child'].search([])
        response = request.render("paceflow.parent_create", {'childs': childs})
        response.headers['X-Frame-Options'] = 'DENY'
        return response

#Parent Submit >>>

    @route(['/my/submit_parent'], type='http', auth='user', website=True)
    def submit_parent(self, **post):
        child_ids = list(map(int, request.httprequest.form.getlist('childs')))
        parent_partner = request.env['res.partner'].sudo().create({
            'name': post.get('firstname'),
            'last_name': post.get('lastname'),
            'email': post.get('email'),
            'phone': post.get('tele_code') + ' ' + post.get('telephone')
            })
        parent_user = request.env['res.users'].sudo().create({
            'name': post.get('firstname') + ' ' + post.get('lastname'),
            'login': post.get('email'),
            'partner_id': parent_partner.id,
            'sel_groups_1_9_10': 9,
        })
        # print('parent_user', parent_user)
        parent = request.env['paceflow.parents'].sudo().create({
            'partner_id': parent_partner.id,
            'email': post.get('email'),
            'phone': post.get('tele_code') + ' ' + post.get('telephone'),
            'emergency_number': post.get('emer_code') + ' ' + post.get('emergency')
        })
        if post['photo']:
            parent_partner.write({
                'image_1920': base64.b64encode(post.get('photo').read()),
            })
            parent_user.write({
                'image_1920': base64.b64encode(post.get('photo').read()),
            })
            parent.write({
                'image_1920': base64.b64encode(post.get('photo').read()),
            })
        if child_ids:
            for child_id in child_ids:
                parent.sudo().write({
                    'child_ids': [(4, child_id)]})

        parent.partner_id.sudo().write({
            'is_parent': True,
        })
        return request.redirect("/my/parent_home")

#Parent Edit >>>>
    @route(['/my/parent_details/<int:parent_id>'], type='http',
           auth='user', website=True)
    def parent_details(self, **kwargs):
        values = {}
        parent = request.env['paceflow.parents'].browse(
            int(kwargs.get('parent_id')))
        parent_child_ids = parent.child_ids
        child_ids = request.env['paceflow.child'].search([
            ('id', 'not in', parent_child_ids.ids)])
        tele = parent.phone.split(" ")
        emer = parent.emergency_number.split(" ")
        values.update({
            'parent': parent,
            'tele_code': tele[0],
            'phone': tele[1],
            'emer_code': emer[0],
            'emergency': emer[1],
            'parent_child': parent_child_ids,
            'child_ids': child_ids
        })
        response = request.render("paceflow.parent_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

#Parent UPDATE >>>>
    @route(['/my/update_parent_details'], type='http',
           auth='user', website=True)
    def update_parent_details(self, **post):
        print("post", post)
        child_ids = list(map(int, request.httprequest.form.getlist('childs')))
        parent = request.env['paceflow.parents'].browse(int(post.get('id')))
        parent_partner = parent.partner_id
        parent_user = request.env['res.users'].search([
            ('partner_id', '=', parent_partner.id)
        ])
        parent_partner.sudo().write({
            'name': post.get('name'),
            'last_name': post.get('lastname'),
            'phone': post.get('tele_code') + ' ' + post.get('phone'),
            'email': post.get('email')
        })
        print(parent_partner)
        parent_user.sudo().write({
            'name': post.get('name'),
            'last_name': post.get('lastname'),
            'login': post.get('email'),
            'partner_id': parent_partner.id,
        })
        parent.sudo().write({
            'email': post.get('email'),
            'phone': post.get('tele_code') + ' ' + post.get('phone'),
            'emergency_number': post.get('emer_code') + ' ' + post.get('emergency')
        })
        if post['photo']:
            parent_partner.write({
                'image_1920': base64.b64encode(post.get('photo').read()),
            })
            parent_user.write({
                'image_1920': base64.b64encode(post.get('photo').read()),
            })
            parent.write({
                'image_1920': base64.b64encode(post.get('photo').read()),
            })

        parent.sudo().write({
            'child_ids': [(5, 0, 0)]})
        if child_ids:
            for child_id in child_ids:
                parent.sudo().write({
                    'child_ids': [(4, child_id)]})
        return request.redirect("/my/parent_home")

# CHILD UPDATE >>>>>

    @route(['/my/submit_details'], type='http', auth='user', website=True)
    def submit_details(self, **post):
        if request.env.user.partner_id.is_client:
            child = request.env['paceflow.child'].sudo().browse(
                                int(post['child_id']))
            group_ids = list(map(int, request.httprequest.form.getlist('groups')))
            parent_ids = list(map(int, request.httprequest.form.getlist('parents')))
            partner = child.partner_id
            partner.write({
                'name': post['name'],
                'last_name': post['lastname'],
                'email': post['email'],
                'phone': post['code'] + ' ' + post['phone'],
                'hand': post.get('hand')
            })
            if post['photo']:
                partner.write({
                    'image_1920': base64.b64encode(post.get('photo').read()),
                })
                child.write({
                    'image_1920': base64.b64encode(post.get('photo').read()),
                })
            child.write({
                'dob': post['dob'],
                'phone': post['code'] + ' ' + post['phone'],
                'email': post['email'],
                'highest_standard': post['highestStd'],
            })
            child.sudo().write({
                'group_ids': [(5, 0, 0)],
                'parent_ids': [(5, 0, 0)]
            })
            if group_ids:
                for group_id in group_ids:
                    child.write({
                        'group_ids': [(4, group_id)]
                    })
            if parent_ids:
                for parent_id in parent_ids:
                    child.write({
                        'parent_ids': [(4, parent_id)]
                    })
            return request.redirect("/my/assessment_report/%s" % child.id)

        elif request.env.user.partner_id.is_parent:
            child = request.env['paceflow.child'].sudo().browse(
                int(post['child_id']))
            partner = child.partner_id
            partner.sudo().write({
                'name': post['name'],
                'last_name': post['lastname'],
                'email': post['email'],
                'phone': post['code'] + ' ' + post['phone'],
                'hand': post.get('hand')
            })
            if post['photo']:
                partner.sudo().write({
                    'image_1920': base64.b64encode(post.get('photo').read()),
                })
                child.sudo().write({
                    'image_1920': base64.b64encode(post.get('photo').read()),
                })
            child.sudo().write({
                'dob': post['dob'],
                'phone': post['code'] + ' ' + post['phone'],
                'email': post['email'],
            })
            return request.redirect("/my/assessment_report/%s" % child.id)

        else:
            return Forbidden()

    @route(['/get_dashboard_data'], type='json', auth='user',
           website=True)
    def get_dashboard_data(self, **post):
        assessment = request.env['assessment.assessment'].sudo().browse(
            int(post['assessment_id'])
        )
        data = {
            'velocity': assessment.velocity,
            'summary_summary_score': int(round(assessment.summary_overall_score)),
            'overall_summary_score': round(assessment.summary_overall_score / 100),
            'legality': round(assessment.new_integer / 100),
            'legality_score': round(assessment.legality_score),
            'summary_legality_score': int(assessment.new_integer),
            'momentum_score': round(assessment.momentum_score / 100),
            'summary_momentum_score': int(round(assessment.momentum_score)),
            'stability_score': round(assessment.stability_score / 100),
            'summary_stability_score': int(round(assessment.stability_score)),
            'paceflow_score': round(assessment.paceflow_score / 100),
            'summary_paceflow_score': int(round(assessment.paceflow_score)),
            'rear_video': assessment.rear_video,
            'rear_reference': assessment.rear_reference,
            'side_video': assessment.side_video,
            'side_reference': assessment.side_reference,
            'img_summary_overall_1': assessment.img_summary_overall_1,
            'img_summary_overall_2': assessment.img_summary_overall_2,
        }

        if assessment.legality_drill_ids:
            legality_drills = []
            for legality_drill in assessment.legality_drill_ids:
                legality_drills.append({'name': legality_drill.name,
                                        'slide_type': legality_drill.slide_type,
                                        'slug': slug(legality_drill),
                                        'url': legality_drill.url})
            data.update({'legality_drills': legality_drills})

        if assessment.momentum_drill_ids:
            momentum_drills = []
            for momentum_drill in assessment.momentum_drill_ids:
                momentum_drills.append({'name': momentum_drill.name,
                                        'slide_type': momentum_drill.slide_type,
                                        'slug': slug(momentum_drill),
                                        'url': momentum_drill.url})
            data.update({'momentum_drills': momentum_drills})

        if assessment.stability_drill_ids:
            obj_rear_stability_drills = request.env['slide.slide'].sudo().search(
                [('id', 'in', assessment.stability_drill_ids.ids),
                 ('stability_rear', '=', True)])
            obj_side_stability_drills = request.env['slide.slide'].sudo().search(
                [('id', 'in', assessment.stability_drill_ids.ids),
                 ('stability_side', '=', True)])
            if obj_rear_stability_drills:
                rear_stability_drills = []
                for stability_drill in obj_rear_stability_drills:
                    rear_stability_drills.append({'name': stability_drill.name,
                                                  'slide_type': stability_drill.slide_type,
                                                  'slug': slug(
                                                      stability_drill),
                                                  'url': stability_drill.url})
                data.update({'rear_stability_drills': rear_stability_drills})
            if obj_side_stability_drills:
                side_stability_drills = []
                for stability_drill in obj_side_stability_drills:
                    side_stability_drills.append({'name': stability_drill.name,
                                                  'slide_type': stability_drill.slide_type,
                                                  'slug': slug(
                                                      stability_drill),
                                                  'url': stability_drill.url})
                data.update({'side_stability_drills': side_stability_drills})
            stability_drills = []
            for stability_drill in assessment.stability_drill_ids:
                stability_drills.append({'name': stability_drill.name,
                                         'slide_type': stability_drill.slide_type,
                                         'slug': slug(stability_drill),
                                         'url': stability_drill.url})
            data.update({'stability_drills': stability_drills})

        if assessment.paceflow_drill_ids:
            obj_rear_paceflow_drills = request.env['slide.slide'].sudo().search(
                [('id', 'in', assessment.paceflow_drill_ids.ids),
                 ('paceflow_rear', '=', True)])
            obj_side_paceflow_drills = request.env['slide.slide'].sudo().search(
                [('id', 'in', assessment.paceflow_drill_ids.ids),
                 ('paceflow_side', '=', True)])
            if obj_rear_paceflow_drills:
                rear_paceflow_drills = []
                for paceflow_drill in obj_rear_paceflow_drills:
                    rear_paceflow_drills.append({'name': paceflow_drill.name,
                                                 'slide_type': paceflow_drill.slide_type,
                                                 'slug': slug(paceflow_drill),
                                                 'url': paceflow_drill.url})
                data.update({'rear_paceflow_drills': rear_paceflow_drills})
            if obj_side_paceflow_drills:
                side_paceflow_drills = []
                for paceflow_drill in obj_side_paceflow_drills:
                    side_paceflow_drills.append({'name': paceflow_drill.name,
                                                 'slide_type': paceflow_drill.slide_type,
                                                 'slug': slug(paceflow_drill),
                                                 'url': paceflow_drill.url})
                data.update({'side_paceflow_drills': side_paceflow_drills})
            paceflow_drills = []
            for paceflow_drill in assessment.paceflow_drill_ids:
                paceflow_drills.append({'name': paceflow_drill.name,
                                        'slide_type': paceflow_drill.slide_type,
                                        'slug': slug(paceflow_drill),
                                        'url': paceflow_drill.url})
            data.update({'paceflow_drills': paceflow_drills})

        if assessment.legality_note_ids:
            legality_notes = []
            for note in assessment.legality_note_ids:
                legality_notes.append({'name': note.name,
                                       'description': note.description})
            data.update({'legality_notes': legality_notes})
        if assessment.momentum_note_ids:
            momentum_notes = []
            for note in assessment.momentum_note_ids:
                momentum_notes.append({'name': note.name,
                                       'description': note.description})
            data.update({'momentum_notes': momentum_notes})
        if assessment.stability_note_ids:

            obj_rear_stability_notes = request.env[
                'comment.comment'].sudo().search(
                [('id', 'in', assessment.stability_note_ids.ids),
                 ('stability_rear', '=', True)])

            obj_side_stability_notes = request.env[
                'comment.comment'].sudo().search(
                [('id', 'in', assessment.stability_note_ids.ids),
                 ('stability_side', '=', True)])

            if obj_rear_stability_notes:
                rear_stability_notes = []
                for note in obj_rear_stability_notes:
                    rear_stability_notes.append({'name': note.name,
                                                 'description': note.description})
                data.update({'rear_stability_notes': rear_stability_notes})
            if obj_side_stability_notes:
                side_stability_notes = []
                for note in obj_side_stability_notes:
                    side_stability_notes.append({'name': note.name,
                                                 'description': note.description})
                data.update({'side_stability_notes': side_stability_notes})
            stability_notes = []
            for note in assessment.stability_note_ids:
                stability_notes.append({'name': note.name,
                                        'description': note.description})
            data.update({'stability_notes': stability_notes})
        if assessment.paceflow_note_ids:

            obj_rear_paceflow_notes = request.env['comment.comment'].sudo().search(
                [('id', 'in', assessment.paceflow_note_ids.ids),
                 ('paceflow_rear', '=', True)])
            obj_side_paceflow_notes = request.env['comment.comment'].sudo().search(
                [('id', 'in', assessment.paceflow_note_ids.ids),
                 ('paceflow_side', '=', True)])

            if obj_rear_paceflow_notes:
                rear_paceflow_notes = []
                for note in obj_rear_paceflow_notes:
                    rear_paceflow_notes.append({'name': note.name,
                                                'description': note.description})
                data.update({'rear_paceflow_notes': rear_paceflow_notes})
            if obj_side_paceflow_notes:
                side_paceflow_notes = []
                for note in obj_side_paceflow_notes:
                    side_paceflow_notes.append({'name': note.name,
                                                'description': note.description})
                data.update({'side_paceflow_notes': side_paceflow_notes})
            paceflow_notes = []
            for note in assessment.paceflow_note_ids:
                paceflow_notes.append({'name': note.name,
                                       'description': note.description})
            data.update({'paceflow_notes': paceflow_notes})
            # print(data.get('paceflow_notes'))
        print('data.get', data.get('legality_drills'))
        return data

#PLAYERS HOME PAGE
    @route(['/my/child_cont', '/child_cont'],
           type='http', auth='user', website=True)
    def child(self):
        if request.env.user.partner_id.is_parent:
            print("haii")
            values = {}
            parent_partner = request.env.user.partner_id
            print("parent", parent_partner)
            parent = request.env['paceflow.parents'].search([
                ('partner_id', '=', parent_partner.id)])
            child_contacts = parent.child_ids
            values.update({
                'parent_view': True,
                'child_contacts': child_contacts,
                'client_view': False
            })
            response = request.render("paceflow.paceflow_child", values)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        elif request.env.user.partner_id.is_client:
            values = {}
            partner = request.env.user.partner_id
            request.env.cr.execute(
                """ SELECT id FROM 
                    paceflow_client WHERE
                    partner_id = %s """, [partner.id])
            client_id = request.env.cr.dictfetchall()
            client = request.env['paceflow.client'].sudo().browse(
                client_id[0]['id'])
            child_contacts = client.child_ids
            values.update({
                'client_view': True,
                'child_contacts': child_contacts,
                'parent_view': False,
            })
            response = request.render("paceflow.paceflow_child", values)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        else:
            return Forbidden()

#CREATE CHILD FORM >>>>>
    @route(['/my/create_child'], type='http', auth='user', website=True)
    def create_child(self):
        groups = request.env['paceflow.child.group'].search([])
        parents = request.env['paceflow.parents'].search([])
        response = request.render("paceflow.create_child_template",
                                  {'groups': groups,
                                   'parents': parents})
        response.headers['X-Frame-Options'] = 'DENY'
        return response

#CREATE CHILD CREATE BUTTON >>>>>
    @route(['/my/create'], type='http', auth='user', website=True)
    def create(self, **post):
        partner = request.env.user.partner_id
        group_ids = list(map(int, request.httprequest.form.getlist('group')))
        parent_ids = list(map(int, request.httprequest.form.getlist('parent')))
        request.env.cr.execute(
            """ SELECT id FROM 
                paceflow_client WHERE
                partner_id = %s """, [partner.id])
        client_id = request.env.cr.dictfetchall()
        client = request.env['paceflow.client'].sudo().browse(
            client_id[0]['id'])
        child_partner = request.env['res.partner'].sudo().create({
            'name': post['name'],
            'last_name': post['lastname'],
            'email': post['email'],
            'phone': post['code'] + ' ' + post['phone'],
            'dob': post['dob'],
        })
        child = request.env['paceflow.child'].sudo().create({
            'partner_id': child_partner.id,
            'email': post['email'],
            'phone': post['code'] + ' ' + post['phone'],
            'dob': post['dob'],
            'highest_standard': post['highestStd'],
        })
        if post['photo']:
            child_partner.write({
                'image_1920': base64.b64encode(post.get('photo').read()),
            })
            child.write({
                'image_1920': base64.b64encode(post.get('photo').read()),
            })
        child_partner.sudo().write({
            'is_child': True,
            'hand': post.get('hand')
        })
        client.sudo().write({
            'child_ids': [(4, child.id)],
        })
        child.sudo().write({
            'coach_ids': [(4, client.id)],
        })
        for group_id in group_ids:
            child.sudo().write({
                'group_ids': [(4, group_id)]
            })
        for parent_id in parent_ids:
            child.sudo().write({
                'parent_ids': [(4, parent_id)]
            })
        return request.redirect("/my/child_cont")

    @route(['/get_filter_data'], type='json', auth='user', website=True)
    def dashboard_onchange(self, **post):
        date_from = datetime.strptime(post['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(post['date_to'], '%Y-%m-%d')
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        assessments = request.env['assessment.assessment'].sudo().search(
            [('child_id', '=', int(child_id)),
                ('stage_id', '=', stage.id), ('report_date', '>=', date_from),
             ('report_date', '<=', date_to)], order='report_date desc',
            limit=10)
        ass_info = []
        for ass in assessments:
            ass_info.append({'id': ass.id, 'name': ass.name})
        return ass_info

    @route(['/get_history_filter_data'], type='json', auth='user', website=True)
    def history_dashboard_onchange(self, **post):
        date_from = datetime.strptime(post['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(post['date_to'], '%Y-%m-%d')
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        assessments = request.env['assessment.assessment'].sudo().search(
            [('child_id', '=', int(child_id)),
             ('stage_id', '=', stage.id), ('done_date', '>=', date_from),
             ('done_date', '<=', date_to)], order='done_date asc',
            limit=10)
        ass_info = []
        for ass in assessments:
            ass_info.append({'id': ass.id, 'name': ass.name})

        return ass_info

    @route(['/get_filter_clear_data'], type='json', auth='user', website=True)
    def dashboard_clear_filter(self, **post):
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        request.env.cr.execute(
            """ SELECT id, name FROM 
                assessment_assessment WHERE
                child_id = %s AND stage_id = %s
                ORDER BY report_date DESC
                LIMIT 10 """, [int(child_id), stage.id])
        ass_info = request.env.cr.dictfetchall()
        return ass_info

    @route(['/get_history_filter_clear_data'], type='json', auth='user',
           website=True)
    def history_dashboard_clear_filter(self, **post):
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)
        request.env.cr.execute(
            """ SELECT id, name FROM 
                assessment_assessment WHERE
                child_id = %s AND stage_id = %s
                ORDER BY done_date ASC
                LIMIT 10 """, [int(child_id), stage.id])
        ass_info = request.env.cr.dictfetchall()
        return ass_info

    @route(['/get_speed_filter_data'], type='json', auth='user', website=True)
    def get_speed_dashboard_data(self, **post):
        date_from = datetime.strptime(post['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(post['date_to'], '%Y-%m-%d')
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        assessments = request.env['assessment.assessment'].sudo().search(
            [('child_id', '=', int(child_id)), ('stage_id', '=', stage.id),
             ('done_date', '>=', date_from), ('done_date', '<=', date_to)],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.velocity)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @route(['/get_score_filter_data'], type='json', auth='user', website=True)
    def get_score_dashboard_data(self, **post):
        date_from = datetime.strptime(post['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(post['date_to'], '%Y-%m-%d')
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        assessments = request.env['assessment.assessment'].sudo().search(
            [('child_id', '=', int(child_id)), ('stage_id', '=', stage.id),
             ('done_date', '>=', date_from), ('done_date', '<=', date_to)],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.summary_overall_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @route(['/get_legality_filter_data'], type='json', auth='user', website=True)
    def get_legality_dashboard_data(self, **post):
        date_from = datetime.strptime(post['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(post['date_to'], '%Y-%m-%d')
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        assessments = request.env['assessment.assessment'].sudo().search(
            [('child_id', '=', int(child_id)), ('stage_id', '=', stage.id),
             ('done_date', '>=', date_from), ('done_date', '<=', date_to)],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.next_integer)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @route(['/get_runup_filter_data'], type='json', auth='user',
           website=True)
    def get_runup_dashboard_data(self, **post):
        date_from = datetime.strptime(post['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(post['date_to'], '%Y-%m-%d')
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        assessments = request.env['assessment.assessment'].sudo().search(
            [('child_id', '=', int(child_id)), ('stage_id', '=', stage.id),
             ('done_date', '>=', date_from), ('done_date', '<=', date_to)],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.run_up_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @route(['/get_stride_filter_data'], type='json', auth='user',
           website=True)
    def get_stride_dashboard_data(self, **post):
        date_from = datetime.strptime(post['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(post['date_to'], '%Y-%m-%d')
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        assessments = request.env['assessment.assessment'].sudo().search(
            [('child_id', '=', int(child_id)), ('stage_id', '=', stage.id),
             ('done_date', '>=', date_from), ('done_date', '<=', date_to)],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.stride_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @route(['/get_ffc_filter_data'], type='json', auth='user',
           website=True)
    def get_ffc_dashboard_data(self, **post):
        date_from = datetime.strptime(post['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(post['date_to'], '%Y-%m-%d')
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        assessments = request.env['assessment.assessment'].sudo().search(
            [('child_id', '=', int(child_id)), ('stage_id', '=', stage.id),
             ('done_date', '>=', date_from), ('done_date', '<=', date_to)],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.ffc_br_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @route(['/get_ft_filter_data'], type='json', auth='user',
           website=True)
    def get_ft_dashboard_data(self, **post):
        date_from = datetime.strptime(post['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(post['date_to'], '%Y-%m-%d')
        child_id = post['child_id']
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        assessments = request.env['assessment.assessment'].sudo().search(
            [('child_id', '=', int(child_id)), ('stage_id', '=', stage.id),
             ('done_date', '>=', date_from), ('done_date', '<=', date_to)],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.br_ft_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

#     Assessment DATA
    @route(['/get_assessment_data'], type='json', auth='user',
           website=True)
    def get_assessment_data(self, **post):
        assessment = request.env['assessment.assessment'].sudo().browse(
            int(post['assessment_id'])
        )
        data = {
            'velocity': assessment.velocity,
            'summary_summary_score': int(round(assessment.summary_overall_score)),
            'overall_summary_score': round(assessment.summary_overall_score / 100),
            'legality': round(assessment.new_integer / 100),
            'legality_score': round(assessment.legality_score),
            'summary_legality_score': int(assessment.new_integer),
            'momentum_score': round(assessment.momentum_score / 100),
            'summary_momentum_score': int(round(assessment.momentum_score)),
            'stability_score': round(assessment.stability_score / 100),
            'summary_stability_score': int(round(assessment.stability_score)),
            'paceflow_score': round(assessment.paceflow_score / 100),
            'summary_paceflow_score': int(round(assessment.paceflow_score)),
            'img_legality_overall': assessment.img_legality_overall,
            'img_momentum_overall': assessment.img_momentum_overall,
            'img_stability_overall_1': assessment.img_stability_overall_1,
            'img_stability_overall_2': assessment.img_stability_overall_2,
            'img_paceflow_overall_1': assessment.img_paceflow_overall_1,
            'img_paceflow_overall_2': assessment.img_paceflow_overall_2,
        }
        if assessment.legality_drill_ids:
            legality_drills = []
            for legality_drill in assessment.legality_drill_ids:
                legality_drills.append({'name': legality_drill.name,
                                        'slide_type': legality_drill.slide_type,
                                        'slug': slug(legality_drill),
                                        'url': legality_drill.url})
            data.update({'legality_drills': legality_drills})
        if assessment.momentum_drill_ids:
            momentum_drills = []
            for momentum_drill in assessment.momentum_drill_ids:
                momentum_drills.append({'name': momentum_drill.name,
                                        'slide_type': momentum_drill.slide_type,
                                        'slug': slug(momentum_drill),
                                        'url': momentum_drill.url})
            data.update({'momentum_drills': momentum_drills})
        if assessment.stability_drill_ids:
            obj_rear_stability_drills = request.env['slide.slide'].sudo().search(
                [('id', 'in', assessment.stability_drill_ids.ids),
                 ('stability_rear', '=', True)])
            obj_side_stability_drills = request.env['slide.slide'].sudo().search(
                [('id', 'in', assessment.stability_drill_ids.ids),
                 ('stability_side', '=', True)])
            if obj_rear_stability_drills:
                rear_stability_drills = []
                for stability_drill in obj_rear_stability_drills:
                    rear_stability_drills.append({'name': stability_drill.name,
                                                  'slide_type': stability_drill.slide_type,
                                                  'slug': slug(
                                                      stability_drill),
                                                  'url': stability_drill.url})
                data.update({'rear_stability_drills': rear_stability_drills})
            if obj_side_stability_drills:
                side_stability_drills = []
                for stability_drill in obj_side_stability_drills:
                    side_stability_drills.append({'name': stability_drill.name,
                                                  'slide_type': stability_drill.slide_type,
                                                  'slug': slug(
                                                      stability_drill),
                                                  'url': stability_drill.url})
                data.update({'side_stability_drills': side_stability_drills})
            stability_drills = []
            for stability_drill in assessment.stability_drill_ids:
                stability_drills.append({'name': stability_drill.name,
                                         'slide_type': stability_drill.slide_type,
                                         'slug': slug(stability_drill),
                                         'url': stability_drill.url})
            data.update({'stability_drills': stability_drills})
        if assessment.paceflow_drill_ids:
            obj_rear_paceflow_drills = request.env['slide.slide'].sudo().search(
                [('id', 'in', assessment.paceflow_drill_ids.ids),
                 ('paceflow_rear', '=', True)])
            obj_side_paceflow_drills = request.env['slide.slide'].sudo().search(
                [('id', 'in', assessment.paceflow_drill_ids.ids),
                 ('paceflow_side', '=', True)])
            if obj_rear_paceflow_drills:
                rear_paceflow_drills = []
                for paceflow_drill in obj_rear_paceflow_drills:
                    rear_paceflow_drills.append({'name': paceflow_drill.name,
                                                 'slide_type': paceflow_drill.slide_type,
                                                 'slug': slug(paceflow_drill),
                                                 'url': paceflow_drill.url})
                data.update({'rear_paceflow_drills': rear_paceflow_drills})
            if obj_side_paceflow_drills:
                side_paceflow_drills = []
                for paceflow_drill in obj_side_paceflow_drills:
                    side_paceflow_drills.append({'name': paceflow_drill.name,
                                                 'slide_type': paceflow_drill.slide_type,
                                                 'slug': slug(paceflow_drill),
                                                 'url': paceflow_drill.url})
                data.update({'side_paceflow_drills': side_paceflow_drills})
            paceflow_drills = []
            for paceflow_drill in assessment.paceflow_drill_ids:
                paceflow_drills.append({'name': paceflow_drill.name,
                                        'slide_type': paceflow_drill.slide_type,
                                        'slug': slug(paceflow_drill),
                                        'url': paceflow_drill.url})
            data.update({'paceflow_drills': paceflow_drills})
        return data
