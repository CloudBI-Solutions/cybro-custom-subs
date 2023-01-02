
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

    @route(['/my/upload'], type='http', auth='user', website=True)
    def upload_form(self, **kw):
        child_id = request.env['paceflow.child'].browse(int(kw.get('child_id')))
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
        response = request.render("paceflow.portal_upload_form", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/form_submit'], type='http', auth='user', website=True)
    def submit_form(self, **post):
        partner = request.env.user.partner_id
        child = request.env['paceflow.child'].sudo().browse(
                            int(post['upload_child_id']))
        if post:
            assessment = request.env['assessment.assessment'].sudo().create({
                'partner_id': partner.id,
                'child_id': child.partner_id.id,
                'highest_standard': post['highest_standard'],
                'dob': child.dob,
                'report_date': fields.Date.today(),
                'name': '%s - %s' % (child.partner_id.name,
                                     fields.Date.today()),
            })
            attachments = request.env['ir.attachment']
            attachment1 = attachments.sudo().create({
                'name': post.get('attachment1').filename,
                'type': 'binary',
                'datas': base64.b64encode(post.get('attachment1').read()),
                'res_model': assessment._name,
                'res_id': assessment.id

            })
            attachment2 = attachments.sudo().create({
                'name': post.get('attachment2').filename,
                'type': 'binary',
                'datas': base64.b64encode(post.get('attachment2').read()),
                'res_model': assessment._name,
                'res_id': assessment.id

            })
            assessment.sudo().write({
                'attachment_ids': [(4, attachment1.id), (4, attachment2.id)],
                'rear_video': attachment1.datas,
                'side_video': attachment2.datas,
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
        print("post", post)
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
            'city': post.get('town'),
            'state_id': int(post.get('state_id')),
            'zip': post.get('phonecode'),
            'country_id': int(post.get('country_id')),
        }
        if post['street']:
            values.update({
                'street2': post['street']
            })
        partner.write(values)
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

    # CHILD DETAILS

    @route(['/my/child_details/<int:child_id>', '/child_details/<int:child_id>'],
           type='http', auth='user', website=True)
    def child_details(self, child_id=None):
        partner = request.env.user.partner_id
        child = request.env['paceflow.child'].sudo().browse(int(child_id))
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
        values = {}

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
        response = request.render("paceflow.portal_child_profile_dashboard", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    # EDIT CHILD

    @route(['/my/edit_child/<int:child_id>'], type='http', auth='user', website=True)
    def edit_child(self, **kwargs):
        print('post', kwargs)
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
        values = {}
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
        response = request.render(
            "paceflow.child_edit_form_template", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    # UPLOAD VIDEO FROM CHILD VIEW

    @route(['/my/upload/<int:child_id>'], type='http', auth='user',
           website=True)
    def upload_video_child(self, **kwargs):
        print("kwargs", kwargs)
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

    @route(['/my/group'], type='http', auth='user', website=True)
    def my_group(self, **post):
        response = request.render("paceflow.group_home")
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/create_group'], type='http', auth='user', website=True)
    def group_create(self, **post):
        response = request.render("paceflow.group_create")
        response.headers['X-Frame-Options'] = 'DENY'
        return response


    @route(['/my/submit_details'], type='http', auth='user', website=True)
    def submit_details(self, **post):
        print("post", post)
        child = request.env['paceflow.child'].sudo().browse(
                            int(post['child_id']))
        print("child", child)
        partner = child.partner_id
        print("partner", partner)
        print(post['code'] + ' ' + post['phone'])
        partner.write({
            'name': post['name'],
            'last_name': post['lastname'],
            'email': post['email'],
            'phone': post['code'] + ' ' + post['phone'],
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
        return request.redirect("/my/child_details/%s" % child.id)

    @route(['/my/child/<int:child_id>', '/child/<int:child_id>'],
           type='http', auth='user', website=True)
    def dashboard(self, child_id=None):
        partner = request.env.user.partner_id
        child = request.env['paceflow.child'].sudo().browse(int(child_id))
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
        values = {}
        stage = request.env['assessment.stage'].sudo().browse(
                request.env.ref('paceflow.stage_done').id)

        request.env.cr.execute(
            """ SELECT id FROM 
                assessment_assessment WHERE
                child_id = %s AND stage_id = %s
                ORDER BY report_date DESC
                LIMIT 10 """, [child_partner.id, stage.id])
        assessments_id = [assessment_id['id']
                          for assessment_id in request.env.cr.dictfetchall()]
        assessments = request.env['assessment.assessment'].sudo().browse(
                                                            assessments_id)
        assessment = assessments[0]
        values.update({
            'partner': partner,
            'child_partner': child_partner,
            'assessments': assessments,
            'assessment': assessment,
            'img_summary1': assessment.img_summary_overall_1,
            'img_summary2': assessment.img_summary_overall_2,
            'img_legality': assessment.img_legality_overall,
            'img_momentum': assessment.img_momentum_overall,
            'img_stability1': assessment.img_stability_overall_1,
            'img_stability2': assessment.img_stability_overall_2,
            'img_paceflow1': assessment.img_paceflow_overall_1,
            'img_paceflow2': assessment.img_paceflow_overall_2,
        })
        response = request.render("paceflow.portal_client_dashboard", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/get_dashboard_data'], type='json', auth='user',
           website=True)
    def get_dashboard_data(self, **post):
        assessment = request.env['assessment.assessment'].sudo().browse(
            int(post['assessment_id'])
        )
        # print("post", post)
        data = {
            'velocity': assessment.velocity,
            'summary_summary_score': int(assessment.summary_overall_score),
            'overall_summary_score': assessment.summary_overall_score / 100,
            'legality': assessment.new_integer / 100,
            'legality_score': assessment.legality_score,
            'summary_legality_score': int(assessment.new_integer),
            'momentum_score': assessment.momentum_score / 100,
            'summary_momentum_score': int(assessment.momentum_score),
            'stability_score': assessment.stability_score / 100,
            'summary_stability_score': int(assessment.stability_score),
            'paceflow_score': assessment.paceflow_score / 100,
            'summary_paceflow_score': int(assessment.paceflow_score),
            'img_phase_1': assessment.img_phase_1,
            'img_phase_2': assessment.img_phase_2,
            'img_phase_3': assessment.img_phase_3,
            'img_phase_4': assessment.img_phase_4,
            'rear_video': assessment.rear_video,
            'side_video': assessment.side_video,
            'img_summary_overall_1': assessment.img_summary_overall_1,
            'img_summary_overall_2': assessment.img_summary_overall_2,
            'img_legality_overall': assessment.img_legality_overall,
            'img_momentum_overall': assessment.img_momentum_overall,
            'img_stability_overall_1': assessment.img_stability_overall_1,
            'img_stability_overall_2': assessment.img_stability_overall_2,
            'img_paceflow_overall_1': assessment.img_paceflow_overall_1,
            'img_paceflow_overall_2': assessment.img_paceflow_overall_2,
        }
        if assessment.drill_ids:
            drills = []
            for drill in assessment.drill_ids:
                drills.append({'name': drill.name,
                               'slide_type': drill.slide_type,
                               'slug': slug(drill)})
            data.update({'drills': drills})
        if assessment.summary_note_ids:
            notes = []
            for note in assessment.summary_note_ids:
                notes.append({'name': note.name,
                              'description': note.description})
            data.update({'notes': notes})
        if assessment.legality_drill_ids:
            legality_drills = []
            for legality_drill in assessment.legality_drill_ids:
                legality_drills.append({'name': legality_drill.name,
                                        'slide_type': legality_drill.slide_type,
                                        'slug': slug(legality_drill)})
            data.update({'legality_drills': legality_drills})
        if assessment.momentum_drill_ids:
            momentum_drills = []
            for momentum_drill in assessment.momentum_drill_ids:
                momentum_drills.append({'name': momentum_drill.name,
                                        'slide_type': momentum_drill.slide_type,
                                        'slug': slug(momentum_drill)})
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
                                                      stability_drill)})
                data.update({'rear_stability_drills': rear_stability_drills})
            if obj_side_stability_drills:
                side_stability_drills = []
                for stability_drill in obj_side_stability_drills:
                    side_stability_drills.append({'name': stability_drill.name,
                                                  'slide_type': stability_drill.slide_type,
                                                  'slug': slug(
                                                      stability_drill)})
                data.update({'side_stability_drills': side_stability_drills})
            stability_drills = []
            for stability_drill in assessment.stability_drill_ids:
                stability_drills.append({'name': stability_drill.name,
                                         'slide_type': stability_drill.slide_type,
                                         'slug': slug(stability_drill)})
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
                for stability_drill in obj_rear_paceflow_drills:
                    rear_paceflow_drills.append({'name': stability_drill.name,
                                                 'slide_type': stability_drill.slide_type,
                                                 'slug': slug(stability_drill)})
                data.update({'rear_paceflow_drills': rear_paceflow_drills})
            if obj_side_paceflow_drills:
                side_paceflow_drills = []
                for stability_drill in obj_side_paceflow_drills:
                    side_paceflow_drills.append({'name': stability_drill.name,
                                                 'slide_type': stability_drill.slide_type,
                                                 'slug': slug(stability_drill)})
                data.update({'side_paceflow_drills': side_paceflow_drills})
            paceflow_drills = []
            for paceflow_drill in assessment.paceflow_drill_ids:
                paceflow_drills.append({'name': paceflow_drill.name,
                                        'slide_type': paceflow_drill.slide_type,
                                        'slug': slug(paceflow_drill)})
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
        return data

    @route(['/my/child_cont', '/child_cont'],
           type='http', auth='user', website=True)
    def child(self):
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
        response = request.render("paceflow.paceflow_child", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/create_child'], type='http', auth='user', website=True)
    def create_child(self):
        response = request.render("paceflow.create_child_template",
                                  {'date': fields.Date.today()})
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/create'], type='http', auth='user', website=True)
    def create(self, **post):
        print("post", post)
        partner = request.env.user.partner_id
        print("partner_id", partner)
        request.env.cr.execute(
            """ SELECT id FROM 
                paceflow_client WHERE
                partner_id = %s """, [partner.id])
        client_id = request.env.cr.dictfetchall()
        print("client_id", client_id)
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
            'highest_standard': post['highestStd']
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
        })
        client.sudo().write({
            'child_ids': [(4, child.id)],
        })
        return request.redirect("/my/home")

    @route(['/get_filter_data'], type='json', auth='user', website=True)
    def dashboard_onchange(self, **post):
        # print("possst", post)
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
        # print("assessments", assessments)
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
