import base64
import json
import io
from odoo.addons.http_routing.models.ir_http import slug
from odoo import fields, _
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager
from collections import OrderedDict
from odoo.http import request, route
from datetime import datetime, date
from odoo.addons.website_sale.controllers.main import WebsiteSale
from dateutil.relativedelta import relativedelta


class Documents(CustomerPortal):

    @http.route(['/my/documents'], type='http',
                auth='user', website=True)
    def documents_home(self, page=0, search='', **post):
        domain = []

        org_domain = []
        if request.env.user.has_group(
                'organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))

        if request.env.user.has_group('organisation.group_organisation_athletes'):
            athlete_id = request.env['organisation.athletes'].search([('partner_id', '=', request.env.user.partner_id.id)])
            domain.append(('athlete_id', '=', athlete_id.id))
            org_domain.append(('id', 'in', athlete_id.organisation_ids.ids))
        elif request.env.user.has_group(
                'organisation.group_organisation_coaches'):
            athlete_id = request.env['organisation.coaches'].search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            domain.append(('coach_id', '=', athlete_id.id))
            org_domain.append(('id', 'in', athlete_id.organisation_ids.ids))
        elif request.env.user.has_group(
                'organisation.group_organisation_parents'):
            parents = request.env['organisation.parents'].search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            athlete_id = parents.mapped('athlete_ids')
            print(parents.organisation_ids)
            domain.append(('athlete_id', 'in', athlete_id.ids))
            org_domain.append(('id', 'in', parents.organisation_ids.ids))
            print(org_domain)
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)

        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        domain.append(('company_id', '=', request.env.user.company_id.id))
        documents = request.env['athletes.documents'].sudo().search(
            domain)
        print(domain)
        total = len(documents)
        pager = request.website.pager(
            url='/my/documents',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        documents = documents[offset: offset + 6]
        values = {
            'search': search,
            'documents': documents,
            'pager': pager,
            'is_account': True,
            'total_documents': request.env[
                'athletes.documents'].sudo().search(
                [('organisation_ids', 'in', organisation.ids)]),
            'organisation': organisation,
            'total': total,
        }
        print('Documents', values)
        return request.render(
            'sports_erp_dashboard.documents_template', values)

    @http.route(['/create/document'], type='http',
                auth='user', website=True)
    def create_document(self, **post):
        coach_ids = list(
            map(int, request.httprequest.form.getlist('document_coach')))
        athlete_ids = list(
            map(int, request.httprequest.form.getlist('document_athlete')))
        group_ids = list(
            map(int, request.httprequest.form.getlist('document_group')))
        org_domain = []
        if request.env.user.has_group(
                'organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        else:
            org_domain.append(
                ('id', 'in', request.env.user.partner_id.organisation_ids.ids))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)

        document = request.env['athletes.documents'].sudo().create({
            'name': post.get('document_name'),
            'description': post.get('document_description'),
            'company_id': request.env.user.company_id.id,
            'document': base64.b64encode(
                    post.get('document_document').read()) if post.get(
                'document_document') else False,
            'organisation_ids': [(4, organisation.id)]
        })
        print(base64.b64encode(
                    post.get('document_document').read()), "kkk")
        attachment = request.env['ir.attachment'].sudo().create({
            'name': post.get('document_document').filename,
            'type': 'binary',
            'datas': base64.b64encode(
                    post.get('document_document').read()) if post.get(
                'document_document') else False,
            'res_model': 'athletes.documents',
            'res_id': document.id
        })
        document.sudo().write({
            'document_id': attachment.id
        })

        for coach in coach_ids:
            request.env['organisation.coaches'].sudo().browse(coach).write({
                'document_ids': [(4, document.id)]
            })
        for athlete in athlete_ids:
            request.env['organisation.athletes'].sudo().browse(athlete).write({
                'document_ids': [(4, document.id)]
            })
        for group in group_ids:
            request.env['athlete.groups'].sudo().browse(group).write({
                'document_ids': [(4, document.id)]
            })
        return request.redirect('/my/documents')

    @http.route(['/my/delete_document/<int:document_id>'], type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def delete_document(self, **kwargs):
        request.env['athletes.documents'].sudo().browse(
            int(kwargs.get('document_id'))).unlink()
        return request.redirect('/my/documents')

    @http.route(['/my/document_details/<int:document_id>'], type='http',
                auth='user', csrf=False, website=True,
                method='POST'
                )
    def document_details(self, **kwargs):
        print('Document details:', kwargs.get('document_id'))
        document = request.env['athletes.documents'].browse(int(kwargs.get('document_id')))
        document.document_id.sudo().generate_access_token()
        return request.render('sports_erp_dashboard.document_details_template', {'document': document, 'is_account': True})

    @http.route(['/attachment/download', ], type='http', auth='user')
    def download_attachments(self, **kw):
        # Check if this is a valid attachment id
        print(kw, "jjjj")
        attachment = request.env['ir.attachment'].sudo().search(
            [('id', '=', int(kw.get('attachment')))])

        if attachment:
            attachment = attachment[0]
        else:
            return request.redirect('/shop')

        if attachment["type"] == "url":
            if attachment["url"]:
                return request.redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = io.BytesIO(base64.standard_b64decode(attachment["datas"]))
            return http.send_file(data, filename=attachment['name'],
                                  as_attachment=True)
        else:
            return request.not_found()

