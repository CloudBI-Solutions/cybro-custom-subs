import base64
import json

from odoo.addons.http_routing.models.ir_http import slug
from odoo import fields, _
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager
from collections import OrderedDict
from odoo.http import request, route
from datetime import datetime, date
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError
from dateutil.relativedelta import relativedelta


class WebsiteSaleSports(WebsiteSale):
    @http.route(['/shop/confirmation'],
                type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        response = super(WebsiteSaleSports,
                         self).shop_payment_confirmation(**post)
        print(post, "post")
        order_lines = response.qcontext['order'].order_line
        partner = response.qcontext['order'].partner_id

        if partner:
            line = order_lines.filtered(
                lambda x: x.product_id.organisation_stage_id)
            if line:
                organisation_partner = partner.sudo().copy()
                organisation_partner.sudo().write({
                    'name': partner.name,
                    'related_partner_id': partner.id,
                })
                organisation = request.env[
                    'organisation.organisation'].sudo().search(
                    [('allowed_user_ids', 'in', [request.env.user.id])])
                print(organisation, "organisations")
                # if not organisation:
                request.env['organisation.organisation'].sudo().create({
                    'partner_id': organisation_partner.id,
                    'name': organisation_partner.company_name if organisation_partner.company_name else organisation_partner.name,
                    'stage_id': line.product_id.organisation_stage_id.id,
                })
            return response


class Organisation(CustomerPortal):

    # HOME

    @route(['/my', '/my/home',
            '/my/home/<model("organisation.organisation"):organisation_id>'],
           type='http', auth="user", website=True)
    def home(self, organisation_id=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        selected_organisation = request.httprequest.cookies.get('selected_organisation')
        print(selected_organisation, "cookies")
        if organisation_id:
            organisations = request.env[
                'organisation.organisation'].sudo().search(
                [('partner_id', '=', partner.id),
                 ('id', '!=', organisation_id.id)])
            for org in organisations:
                org.sudo().is_selected_organisation = False
            organisation_id.is_selected_organisation = True
        else:
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                ['|', ('partner_id', '=', partner.id),
                 ('id', '=', selected_organisation)], limit=1)
            print(organisation)
            organisation.is_selected_organisation = True

        domain = []
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        print(organisation)
        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))

        domain.append(('company_id', '=', request.env.user.company_id.id))
        home_images = request.env['home.image'].sudo().search(
            domain)
        gallery_images = request.env['home.gallery'].sudo().search(domain)
        values.update({
            'partner': partner,
            'is_account': True,
            'home_images': home_images,
            'gallery_images': gallery_images,
        })
        return request.render("sports_erp_dashboard.sports_erp_portal", values)

        # Dashboard

    @route(['/my/settings', '/settings'], type='http', auth='user',
           website=True)
    def settings_dashboard(self):
        """RENDER SETTINGS PAGE TEMPLATE"""
        response = request.render("sports_erp_dashboard.settings_dashboard",
                                  {'is_account': True})
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @http.route(['/my/invoices', '/my/invoices/page/<int:page>'], type='http',
                auth="user", website=True)
    def portal_my_invoices(self, page=1, date_begin=None, date_end=None,
                           sortby=None, filterby=None, **kw):
        """RENDER INVOICES"""
        if request.env.user.partner_id.org_group_selection == 'organisation':
            partner = request.env.user.partner_id
            values = self._prepare_portal_layout_values()
            organisation = request.env[
                'organisation.organisation'].sudo().search([
                ('partner_id', '=', partner.id)
            ])
            # childs = parent.child_ids
            # child_partners = childs.mapped('partner_id')
            AccountInvoice = request.env['account.move']
            domain = self._get_invoices_domain()
            domain += [(
                'partner_id', 'in', [organisation.partner_id.id, organisation.partner_id.related_partner_id])]
            print(domain, "domain")
            searchbar_sortings = {
                'date': {'label': _('Date'), 'order': 'invoice_date desc'},
                'duedate': {'label': _('Due Date'),
                            'order': 'invoice_date_due desc'},
                'name': {'label': _('Reference'), 'order': 'name desc'},
                'state': {'label': _('Status'), 'order': 'state'},
            }
            # default sort by order
            if not sortby:
                sortby = 'date'
            order = searchbar_sortings[sortby]['order']

            searchbar_filters = {
                'all': {'label': _('All'), 'domain': []},
                'invoices': {'label': _('Invoices'), 'domain': [
                    ('move_type', '=', ('out_invoice', 'out_refund'))]},
                'bills': {'label': _('Bills'), 'domain': [
                    ('move_type', '=', ('in_invoice', 'in_refund'))]},
            }
            # default filter by value
            if not filterby:
                filterby = 'all'
            domain += searchbar_filters[filterby]['domain']

            if date_begin and date_end:
                domain += [('create_date', '>', date_begin),
                           ('create_date', '<=', date_end)]

            # count for pager
            invoice_count = AccountInvoice.sudo().search_count(domain)
            # pager
            pager = portal_pager(
                url="/my/invoices",
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby},
                total=invoice_count,
                page=page,
                step=self._items_per_page
            )
            # content according to pager and archive selected
            invoices = AccountInvoice.sudo().search(
                domain, order=order,
                limit=self._items_per_page,
                offset=pager['offset'])
            request.session['my_invoices_history'] = invoices.ids[:100]
            values.update({
                'date': date_begin,
                'invoices': invoices,
                'page_name': 'invoice',
                'pager': pager,
                'default_url': '/my/invoices',
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
                'searchbar_filters': OrderedDict(
                    sorted(searchbar_filters.items())),
                'filterby': filterby,
                'is_account': True
            })
            return request.render("account.portal_my_invoices", values)

        # elif request.env.user.partner_id.is_child:
        #     child_partner = request.env.user.partner_id
        #     child = request.env['paceflow.child'].search([
        #         ('partner_id', '=', child_partner.id)
        #     ])
        #     difference = relativedelta(date.today(), child.dob)
        #     if int(difference.years) >= 18:
        #         values = self._prepare_portal_layout_values()
        #         AccountInvoice = request.env['account.move']
        #         domain = self._get_invoices_domain()
        #         domain += [(
        #             'partner_id', '=', child_partner.id)]
        #         searchbar_sortings = {
        #             'date': {'label': _('Date'), 'order': 'invoice_date desc'},
        #             'duedate': {'label': _('Due Date'),
        #                         'order': 'invoice_date_due desc'},
        #             'name': {'label': _('Reference'), 'order': 'name desc'},
        #             'state': {'label': _('Status'), 'order': 'state'},
        #         }
        #         # default sort by order
        #         if not sortby:
        #             sortby = 'date'
        #         order = searchbar_sortings[sortby]['order']
        #
        #         searchbar_filters = {
        #             'all': {'label': _('All'), 'domain': []},
        #             'invoices': {'label': _('Invoices'), 'domain': [
        #                 ('move_type', '=', ('out_invoice', 'out_refund'))]},
        #             'bills': {'label': _('Bills'), 'domain': [
        #                 ('move_type', '=', ('in_invoice', 'in_refund'))]},
        #         }
        #         # default filter by value
        #         if not filterby:
        #             filterby = 'all'
        #         domain += searchbar_filters[filterby]['domain']
        #
        #         if date_begin and date_end:
        #             domain += [('create_date', '>', date_begin),
        #                        ('create_date', '<=', date_end)]
        #
        #         # count for pager
        #         invoice_count = AccountInvoice.sudo().search_count(domain)
        #         # pager
        #         pager = portal_pager(
        #             url="/my/invoices",
        #             url_args={'date_begin': date_begin, 'date_end': date_end,
        #                       'sortby': sortby},
        #             total=invoice_count,
        #             page=page,
        #             step=self._items_per_page
        #         )
        #         # content according to pager and archive selected
        #         invoices = AccountInvoice.sudo().search(
        #             domain, order=order,
        #             limit=self._items_per_page,
        #             offset=pager['offset'])
        #         request.session['my_invoices_history'] = invoices.ids[:100]
        #         values.update({
        #             'date': date_begin,
        #             'invoices': invoices,
        #             'page_name': 'invoice',
        #             'pager': pager,
        #             'default_url': '/my/invoices',
        #             'searchbar_sortings': searchbar_sortings,
        #             'sortby': sortby,
        #             'searchbar_filters': OrderedDict(
        #                 sorted(searchbar_filters.items())),
        #             'filterby': filterby,
        #         })
        #         return request.render("account.portal_my_invoices", values)
        #     else:
        #         response = request.render("paceflow.portal_forbidden")
        #         response.headers['X-Frame-Options'] = 'DENY'
        #         return response
        #
        # elif request.env.user.partner_id.is_client:
        #     coach_partner = request.env.user.partner_id
        #     values = self._prepare_portal_layout_values()
        #     coach = request.env['paceflow.client'].sudo().search([
        #         ('partner_id', '=', coach_partner.id)
        #     ])
        #     childs = coach.child_ids
        #     child_partners = childs.mapped('partner_id')
        #     parents = request.env['paceflow.parents'].sudo().search([
        #         ('created_coach', '=', coach.id)
        #     ])
        #     parent_partners = parents.mapped('partner_id')
        #     AccountInvoice = request.env['account.move']
        #     domain = self._get_invoices_domain()
        #     domain += [
        #         ('partner_id', 'in',
        #          coach_partner.ids + child_partners.ids + parent_partners.ids)]
        #     searchbar_sortings = {
        #         'date': {'label': _('Date'), 'order': 'invoice_date desc'},
        #         'duedate': {'label': _('Due Date'),
        #                     'order': 'invoice_date_due desc'},
        #         'name': {'label': _('Reference'), 'order': 'name desc'},
        #         'state': {'label': _('Status'), 'order': 'state'},
        #     }
        #     # default sort by order
        #     if not sortby:
        #         sortby = 'date'
        #     order = searchbar_sortings[sortby]['order']
        #
        #     searchbar_filters = {
        #         'all': {'label': _('All'), 'domain': []},
        #         'invoices': {'label': _('Invoices'), 'domain': [
        #             ('move_type', '=', ('out_invoice', 'out_refund'))]},
        #         'bills': {'label': _('Bills'), 'domain': [
        #             ('move_type', '=', ('in_invoice', 'in_refund'))]},
        #     }
        #     # default filter by value
        #     if not filterby:
        #         filterby = 'all'
        #     domain += searchbar_filters[filterby]['domain']
        #
        #     if date_begin and date_end:
        #         domain += [('create_date', '>', date_begin),
        #                    ('create_date', '<=', date_end)]
        #
        #     # count for pager
        #     invoice_count = AccountInvoice.sudo().search_count(domain)
        #     # pager
        #     pager = portal_pager(
        #         url="/my/invoices",
        #         url_args={'date_begin': date_begin, 'date_end': date_end,
        #                   'sortby': sortby},
        #         total=invoice_count,
        #         page=page,
        #         step=self._items_per_page
        #     )
        #     # content according to pager and archive selected
        #     invoices = AccountInvoice.sudo().search(domain, order=order,
        #                                             limit=self._items_per_page,
        #                                             offset=pager['offset'])
        #     request.session['my_invoices_history'] = invoices.ids[:100]
        #     values.update({
        #         'date': date_begin,
        #         'invoices': invoices,
        #         'page_name': 'invoice',
        #         'pager': pager,
        #         'default_url': '/my/invoices',
        #         'searchbar_sortings': searchbar_sortings,
        #         'sortby': sortby,
        #         'searchbar_filters': OrderedDict(
        #             sorted(searchbar_filters.items())),
        #         'filterby': filterby,
        #     })
        #     return request.render("account.portal_my_invoices", values)

    @route(['/my/dashboard'], type='http', auth="user", website=True)
    def my_dashboard(self):
        login_user = request.env.user.partner_id
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        members = request.env['res.partner'].sudo().search(
            [('id', '!=', organisation.partner_id.id),
             ('organisation_ids', 'in', [organisation.id]),
             ('company_id', '=', request.env.user.company_id.id)])
        values = {
            'user': login_user,
            'is_account': True,
            'organisation': organisation,
            'members': members,
        }
        return request.render("sports_erp_dashboard.sports_erp_dashboard",
                              values)

    # COACHES
    @http.route(['/my/coaches', '/my/coaches/page/<int:page>'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def my_coaches(self, page=0, search='', **post):
        if not request.env.user.has_group('organisation.group_organisation_administrator') and not request.env.user.has_group('organisation.group_organisation_athletes'):
            raise AccessError(_("You don't have enough access rights to run this action."))
        domain = []
        assign_domain = []
        tag_ids = list(
            map(int, request.httprequest.form.getlist('filtered_tags')))
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))
            assign_domain.append(('organisation_ids', 'in', [organisation.id]))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        if post.get('price-min'):
            domain.append(('price_o2o', '>=', float(post['price-min'])))
        if post.get('price-max'):
            domain.append(('price_o2o', '<=', float(post['price-max'])))
        if post.get('team-min'):
            domain.append(('price_team', '>=', float(post['team-min'])))
        if post.get('team-max'):
            domain.append(('price_team', '<=', float(post['team-max'])))
        if tag_ids:
            domain.append(('tag_ids', 'in', tag_ids))
        lowest_price = 0.00
        highest_price = 0.00
        team_session_low = 0.00
        team_session_high = 0.00
        if request.env.user.partner_id.org_group_selection == 'athletes':
            athlete = request.env['organisation.athletes'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            domain.append(('id', 'in', athlete.coach_ids.ids))
        coaches = request.env['organisation.coaches'].sudo().search(domain)
        if coaches:
            prices = coaches.mapped(lambda x: x.price_o2o)
            team_session = coaches.mapped(lambda x: x.price_team)
            team_session_low = min(team_session)
            team_session_high = max(team_session)
            lowest_price = min(prices)
            highest_price = max(prices)
        athletes = request.env['organisation.athletes'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        parents = request.env['organisation.parents'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        groups = request.env['athlete.groups'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        disciplines = request.env['organisation.discipline'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        total = len(coaches)
        pager = request.website.pager(
            url='/my/coaches',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        coaches = coaches[offset: offset + 5]
        values = {
            'search': search,
            'coaches': coaches,
            'athletes': athletes,
            'parents': parents,
            'groups': groups,
            'disciplines': disciplines,
            'pager': pager,
            'is_account': True,
            'organisations': request.env['organisation.organisation'].sudo().search([('allowed_user_ids', 'in', [request.env.user.id])]),
            'total_coaches': coaches,
            'total': total,
            'highest_price': float(post.get('price-max')) if post.get(
                'price-max') else highest_price,
            'lowest_price': float(post.get('price-min')) if post.get(
                'price-min') else lowest_price,
            'team_session_low': float(post.get('team-min')) if post.get(
                'team-min') else team_session_low,
            'team_session_high': float(post.get('team-max')) if post.get(
                'team-max') else team_session_high,
            'filtered_tags': request.env[
                'coaches.tags'].sudo().browse(tag_ids),
            'subscriptions': request.env['product.product'].sudo().search([
                                      ('organisation_ids', 'in',
                                       [organisation.id]),
                                      ('company_id', '=',
                                       request.env.user.company_id.id)]),
            'booking_types': request.env['booking.type'].sudo().search([]),
            'channels': request.env['chat.hub'].sudo().search([]),
        }
        return request.render('sports_erp_dashboard.coach_dashboard_template',
                              values)

    @http.route('/create/coach', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def create_coach(self, **post):
        if post:
            coach_partner = request.env['res.partner'].sudo().create({
                'name': post.get('coach_name'),
                'last_name': post.get('last_name'),
                'email': post.get('email'),
                'phone': post.get('phone')
            })
            tag_ids = list(
                map(int, request.httprequest.form.getlist('tags')))
            organisation_ids = list(
                map(int, request.httprequest.form.getlist('organisations')))
            athlete_ids = list(
                map(int, request.httprequest.form.getlist('athletes')))
            group_ids = list(
                map(int, request.httprequest.form.getlist('groups')))
            discipline_ids = list(
                map(int, request.httprequest.form.getlist('disciplines')))
            document_ids = list(
                map(int, request.httprequest.form.getlist('documents')))
            org_domain = []
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
            if request.httprequest.cookies.get('select_organisation') is not None:
                org_domain.append(('id', '=',
                                   request.httprequest.cookies.get(
                                       'select_organisation')))
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1)
            organisation_ids.append(organisation.id)
            values = {
                'partner_id': coach_partner.id,
                'phone': post.get('phone'),
                'email': post.get('email'),
                'create_booking': post.get('booking'),
                'price_o2o': post.get('onetoprice'),
                'price_team': post.get('teamprice'),
                'tag_ids': [(4, tag) for tag in tag_ids],
                'organisation_ids': [(4, org) for org in organisation_ids],
                'group_ids': [(4, group) for group in group_ids],
                'discipline_ids': [(4, discipline) for discipline in
                                   discipline_ids],
                'athlete_ids': [(4, athlete) for athlete in athlete_ids],
                'document_ids': [(4, document) for document in document_ids],
                'company_id': request.env.user.company_id.id,
            }
            coach = request.env['organisation.coaches'].sudo().create(values)
            coach.partner_id.write({
                'create_booking': True if post.get(
                    'booking') == 'on' else False,
                'image_1920': base64.b64encode(
                    post.get('photo').read()) if post.get('photo') else False,
                'organisation_ids': [(4, org) for org in organisation_ids],
                'company_id': request.env.user.company_id.id,
            })
            return request.redirect('/my/coaches')

    @http.route('/remove/coach/<model("organisation.coaches"):coach_id>',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_coach(self, coach_id=None):
        if coach_id:
            coach_id.sudo().unlink()
        return request.redirect('/my/coaches')

    @http.route('/my/coach/<model("organisation.coaches"):coach_id>',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def coach_details(self, coach_id=None):
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        athletes = request.env['organisation.athletes'].sudo().search([('organisation_ids', 'in', [organisation.id])])
        parents = request.env['organisation.parents'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        # coaches = request.env['organisation.coaches'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        groups = request.env['athlete.groups'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        disciplines = request.env['organisation.discipline'].sudo().search(
            [('organisation_ids', 'in', [organisation.id])])
        values = {
            'coach': coach_id,
            'is_account': True,
            'organisations': request.env[
                'organisation.organisation'].sudo().search(
                [('allowed_user_ids', 'in', [request.env.user.id])]),
            'athletes': athletes,
            'groups': groups,
            'parents': parents,
            'disciplines': disciplines,


        }
        return request.render(
            'sports_erp_dashboard.coach_dashboard_details_template', values)

    @http.route('/update',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def update_coach(self, **post):
        print(post, "post")
        tag_ids = list(
            map(int, request.httprequest.form.getlist('tags')))
        organisation_ids = list(
            map(int, request.httprequest.form.getlist('organisations')))
        athlete_ids = list(
            map(int, request.httprequest.form.getlist('athletes')))
        group_ids = list(
            map(int, request.httprequest.form.getlist('groups')))
        document_ids = list(
            map(int, request.httprequest.form.getlist('documents')))
        discipline_ids = list(
            map(int, request.httprequest.form.getlist('disciplines')))
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        organisation_ids.append(organisation.id)
        values = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'discipline_ids': [(4, discipline) for discipline in
                               discipline_ids],
            'price_o2o': post.get('onetoprice'),
            'price_team': post.get('teamprice'),
            'athlete_ids': [(4, athlete) for athlete in athlete_ids],
            'tag_ids': [(4, tag) for tag in tag_ids],
            'organisation_ids': [(4, organisation) for organisation in
                                 organisation_ids],
            'group_ids': [(4, group) for group in group_ids],
            'document_ids': [(4, document) for document in document_ids],
        }
        if post.get('coach'):
            coach = request.env['organisation.coaches'].sudo().browse(
                int(post.get('coach')))
            if coach:
                coach.sudo().write({
                    'discipline_ids': [(5, 0, 0)],
                    'athlete_ids': [(5, 0, 0)],
                    'tag_ids': [(5, 0, 0)],
                    'organisation_ids': [(5, 0, 0)],
                    'group_ids': [(5, 0, 0)],
                    'document_ids': [(5, 0, 0)],
                })
                coach.partner_id.sudo().write({
                    'name': post.get('name'),
                    'last_name': post.get('last_name'),
                    'email': post.get('email'),
                    'phone': post.get('phone'),
                    'height': post.get('height'),
                    'weight': post.get('weight'),
                    'image_1920': base64.b64encode(
                        post.get('photo').read()) if post.get('photo') else False
                })
            coach.sudo().write(values)
        return request.redirect('/my/coach/%s' % coach.id)

    @http.route(['/my/athletes/home', '/my/athletes/home/page/<int:page>'],
                type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def my_athletes_home(self, page=0, search='', **post):
        coach_ids = list(
            map(int, request.httprequest.form.getlist('filtered_coaches')))
        print('coaches_ids', coach_ids)
        tag_ids = list(
            map(int, request.httprequest.form.getlist('filtered_tags')))
        print('tag_ids', tag_ids)
        parent_ids = list(
            map(int, request.httprequest.form.getlist('filtered_parents')))
        print('parent_ids', parent_ids)

        domain = []
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        if coach_ids:
            domain.append(('coach_ids', 'in', coach_ids))
        if tag_ids:
            domain.append(('tag_ids', 'in', tag_ids))
        if parent_ids:
            domain.append(('parent_ids', 'in', parent_ids))
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        print(request.env.user.partner_id.org_group_selection)
        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))
        if request.env.user.partner_id.org_group_selection == 'parents':
            parents = request.env['organisation.parents'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            domain.append(('id', 'in', parents.athlete_ids.ids))
        elif request.env.user.partner_id.org_group_selection == 'ex_coaches':
            coaches = request.env['organisation.coaches'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            domain.append(('id', 'in', coaches.athlete_ids.ids))
        athletes = request.env['organisation.athletes'].sudo().search(domain)
        parents = request.env['organisation.parents'].sudo().search([('organisation_ids', 'in', [organisation.id])])
        coaches = request.env['organisation.coaches'].sudo().search([('organisation_ids', 'in', [organisation.id])])
        groups = request.env['athlete.groups'].sudo().search([('organisation_ids', 'in', [organisation.id])])
        disciplines = request.env['organisation.discipline'].sudo().search([('organisation_ids', 'in', [organisation.id])])
        total = len(athletes)
        pager = request.website.pager(
            url='/my/athletes/home',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        athletes = athletes[offset: offset + 5]
        return request.render('sports_erp_dashboard.athlete_dashboard_template',
                              {
                                  'search': search,
                                  'athletes': athletes,
                                  'pager': pager,
                                  'is_account': True,
                                  'organisations': request.env[
                                      'organisation.organisation'].sudo().search(
                                      [('allowed_user_ids', 'in',
                                        [request.env.user.id])]),
                                  'parents': parents,
                                  'coaches': coaches,
                                  'groups': groups,
                                  'disciplines': disciplines,
                                  'total_athletes': athletes,
                                  'total': total,
                                  'filtered_coaches': request.env[
                                      'organisation.coaches'].sudo().browse(
                                      coach_ids),
                                  'filtered_tags': request.env[
                                      'athletes.tags'].sudo().browse(tag_ids),
                                  'filtered_parents': request.env[
                                      'organisation.parents'].sudo().browse(
                                      parent_ids),
                                  'subscriptions': request.env[
                                      'product.product'].sudo().search([
                                      ('organisation_ids', 'in',
                                       [organisation.id]),
                                      ('company_id', '=',
                                       request.env.user.company_id.id)]),
                                  'booking_types': request.env[
                                      'booking.type'].sudo().search([]),
                                  'channels': request.env[
                                      'chat.hub'].sudo().search([]),
                              })

    @http.route('/create/athlete', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def create_athlete(self, **post):
        if post:
            print('post', post)
            tag_ids = list(
                map(int, request.httprequest.form.getlist('tags')))
            organisation_ids = list(
                map(int, request.httprequest.form.getlist('organisations')))
            parent_ids = list(
                map(int, request.httprequest.form.getlist('parents')))
            coach_ids = list(
                map(int, request.httprequest.form.getlist('coaches')))
            group_ids = list(
                map(int, request.httprequest.form.getlist('groups')))
            product_ids = list(
                map(int, request.httprequest.form.getlist('products')))
            discipline_ids = list(
                map(int, request.httprequest.form.getlist('disciplines')))
            org_domain = []
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
            if request.httprequest.cookies.get(
                    'select_organisation') is not None:
                org_domain.append(('id', '=',
                                   request.httprequest.cookies.get(
                                       'select_organisation')))
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1)
            organisation_ids.append(organisation.id)
            athlete_partner = request.env['res.partner'].sudo().create({
                'name': post.get('athlete_name'),
                'last_name': post.get('last_name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'organisation_ids': [(4, organisation) for organisation in
                                     organisation_ids],
                'company_id': request.env.company.id
            })

            values = {
                'partner_id': athlete_partner.id,
                'phone': post.get('phone'),
                'email': post.get('email'),
                'member_id': post.get('member_id'),
                'dob': post.get('dob'),
                'tag_ids': [(4, tag) for tag in tag_ids],
                'organisation_ids': [(4, organisation) for organisation in
                                     organisation_ids],
                'group_ids': [(4, group) for group in group_ids],
                'parent_ids': [(4, parent) for parent in parent_ids],
                'product_ids': [(4, product) for product in product_ids],
                'coach_ids': [(4, coach) for coach in coach_ids],
                'discipline_ids': [(4, discipline) for discipline in
                                   discipline_ids],
            }
            athlete = request.env['organisation.athletes'].sudo().create(values)
            athlete.partner_id.write({
                'create_booking': True if post.get(
                    'booking') == 'on' else False,
                'image_1920': base64.b64encode(
                    post.get('photo').read()) if post.get('photo') else False
            })
            return request.redirect('/my/athletes/home')

    @http.route('/remove/<model("organisation.athletes"):athlete_id>',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_athlete(self, athlete_id=None):
        if athlete_id:
            athlete_id.sudo().unlink()
        return request.redirect('/my/athletes/home')

    @http.route('/my/athlete/<model("organisation.athletes"):athlete_id>',
                type='http',
                auth='user', csrf=False, website=True,
                method='GET')
    def athlete_details(self, athlete_id=None):
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        disciplines = request.env['organisation.discipline'].search(
                [('organisation_ids', 'in', organisation.id)])
        coaches = request.env['organisation.coaches'].search(
            [('organisation_ids', 'in', organisation.id)])
        parents = request.env['organisation.parents'].search(
            [('organisation_ids', 'in', organisation.id)])
        values = {
            'athlete': athlete_id,
            'is_account': True,
            'organisations': request.env[
                'organisation.organisation'].sudo().search(
                [('allowed_user_ids', 'in',
                  [request.env.user.id])]),
            'disciplines': disciplines,
            'coaches': coaches,
            'parents': parents,
        }
        return request.render(
            'sports_erp_dashboard.athlete_dashboard_details_template', values)

    @http.route('/update/athlete',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def update_athlete(self, **post):
        print(post, "posttttt")
        tag_ids = list(
            map(int, request.httprequest.form.getlist('tags')))
        organisation_ids = list(
            map(int, request.httprequest.form.getlist('organisations')))
        parent_ids = list(
            map(int, request.httprequest.form.getlist('parents')))
        coach_ids = list(
            map(int, request.httprequest.form.getlist('coaches')))
        group_ids = list(
            map(int, request.httprequest.form.getlist('groups')))
        product_ids = list(
            map(int, request.httprequest.form.getlist('products')))
        discipline_ids = list(
            map(int, request.httprequest.form.getlist('disciplines')))
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        organisation_ids.append(organisation.id)
        values = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'member_id': post.get('member_id'),
            'discipline_ids': [(4, discipline) for discipline in
                               discipline_ids],
            'parent_ids': [(4, parent) for parent in parent_ids],
            'tag_ids': [(4, tag) for tag in tag_ids],
            'organisation_ids': [(4, organisation) for organisation in
                                 organisation_ids],
            'group_ids': [(4, group) for group in group_ids],
            'product_ids': [(4, product) for product in product_ids],
            'coach_ids': [(4, coach) for coach in coach_ids],
        }
        athlete = request.env['organisation.athletes'].sudo().browse(
            int(post.get('athlete')))
        print(post, "athlete")
        if athlete:
            athlete.sudo().write({
                'discipline_ids': [(5, 0, 0)],
                'parent_ids': [(5, 0, 0)],
                'tag_ids': [(5, 0, 0)],
                'organisation_ids': [(5, 0, 0)],
                'group_ids': [(5, 0, 0)],
                'product_ids': [(5, 0, 0)],
                'coach_ids': [(5, 0, 0)],
            })
            athlete.partner_id.sudo().write({
                'name': post.get('name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'height': post.get('height'),
                'weight': post.get('weight'),
                'image_1920': base64.b64encode(
                    post.get('photo').read()) if post.get('photo') else False
            })
            athlete.sudo().write(values)
        return request.redirect('/my/athlete/%s' % athlete.id)

    # PARENTS

    @http.route(['/my/parents', '/my/parents/page/<int:page>'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def my_parents(self, page=0, search='', **post):
        if request.env.user._is_public():
            return request.redirect('/web/login')
        tag_ids = list(
            map(int, request.httprequest.form.getlist('filtered_tags')))
        domain = []
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        if tag_ids:
            domain.append(('tag_ids', 'in', tag_ids))
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))
        if request.env.user.partner_id.org_group_selection == 'athletes':
            athlete = request.env['organisation.athletes'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            domain.append(('id', 'in', athlete.parent_ids.ids))
        parents = request.env['organisation.parents'].sudo().search(domain)
        print('parents', parents)
        total = len(parents)
        pager = request.website.pager(
            url='/my/parents',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        parents = parents[offset: offset + 5]
        return request.render('sports_erp_dashboard.parents_dashboard_template',
                              {
                                  'search': search,
                                  'parents': parents,
                                  'total_parents': parents,
                                  'organisations': request.env[
                'organisation.organisation'].sudo().search(
                [('allowed_user_ids', 'in',
                  [request.env.user.id])]),
                                  'athletes': request.env[
                'organisation.athletes'].sudo().search(
                [('organisation_ids', 'in',
                  [organisation.id])]),
                                  'pager': pager,
                                  'is_account': True,
                                  'total': total,
                                  'filtered_tags': request.env[
                                      'parents.tags'].sudo().browse(tag_ids),
                                  'subscriptions': request.env['product.product'].sudo().search([
                                      ('organisation_ids', 'in',
                                       [organisation.id]),
                                      ('company_id', '=',
                                       request.env.user.company_id.id)]),
                                    'booking_types': request.env['booking.type'].sudo().search([]),
                                    'channels': request.env['chat.hub'].sudo().search([]),
                              })

    @http.route('/create/parent', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def create_parent(self, **post):
        if post:
            print(post, "post....")
            tag_ids = list(
                map(int, request.httprequest.form.getlist('tags')))
            organisation_ids = list(
                map(int, request.httprequest.form.getlist('organisations')))
            athlete_ids = list(
                map(int, request.httprequest.form.getlist('athletes')))
            org_domain = []
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
            if request.httprequest.cookies.get(
                    'select_organisation') is not None:
                org_domain.append(('id', '=',
                                   request.httprequest.cookies.get(
                                       'select_organisation')))
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1)
            if organisation:
                organisation_ids.append(organisation.id)
            parent_partner = request.env['res.partner'].sudo().create({
                'name': post.get('parent_name'),
                'last_name': post.get('last_name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'organisation_ids': [(4, org) for org in organisation_ids],
                'company_id': request.env.user.company_id.id
            })

            values = {
                'partner_id': parent_partner.id,
                'phone': post.get('phone'),
                'email': post.get('email'),
                'tag_ids': [(4, tag) for tag in tag_ids],
                'organisation_ids': [(4, org) for org in organisation_ids],
                'athlete_ids': [(4, athlete) for athlete in athlete_ids],
            }
            if post.get('responsible'):
                values.update({
                    'responsible_user_id': int(post.get('responsible')),
                })
            parent = request.env['organisation.parents'].sudo().create(values)
            parent.partner_id.write({
                'create_booking': True if post.get(
                    'booking') == 'on' else False,
            })
            return request.redirect('/my/parents')

    @http.route('/remove/parent/<model("organisation.parents"):parent_id>',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_parent(self, parent_id=None):
        if parent_id:
            parent_id.sudo().unlink()
        return request.redirect('/my/parents')

    @http.route('/my/parent/<model("organisation.parents"):parent_id>',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def parent_details(self, parent_id=None):
        values = {
            'parent': parent_id,
            'is_account': True
        }
        return request.render(
            'sports_erp_dashboard.parent_dashboard_details_template', values)

    @http.route(['/my/update_parent'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def update_parent(self, **post):
        parent = request.env[
            'organisation.parents'].sudo().browse(
            int(post.get('parent')))
        parent.sudo().write({
            'name': post.get('name'),
            'phone': post.get('phone'),
            # 'date': post.get('date'),
            'email': post.get('email'),
            # 'responsible_user_id': int(
            #     post.get('responsible_user')) if post.get(
            #     'responsible_user') else None,
        })
        parent.sudo().partner_id.write({
            'name': post.get('name'),
            'phone': post.get('phone'),
            'email': post.get('email'),
        })
        parent.sudo().write({
            'tag_ids': [(5, 0, 0)],
            'organisation_ids': [(5, 0, 0)]
        })
        tag_ids = list(
            map(int, request.httprequest.form.getlist('tags')))
        if tag_ids:
            parent.sudo().write({
                'tag_ids': [(4, tag) for tag in tag_ids]
            })
        org_ids = list(
            map(int, request.httprequest.form.getlist('organisation')))
        if org_ids:
            parent.sudo().write({
                'organisation_ids': [(4, org) for org in org_ids]
            })
        return request.redirect('/my/parent/%s' % parent.id)

    @http.route(['/my/groups', '/my/groups/page/<int:page>'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def my_groups(self, page=0, search='', **post):
        print("self....", search)
        tag_ids = list(
            map(int, request.httprequest.form.getlist('filtered_tags')))
        domain = []
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        if tag_ids:
            domain.append(('tag_ids', 'in', tag_ids))
        org_domain = []
        if request.env.user.has_group('organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.env.user.has_group('organisation.group_organisation_coaches'):
            coach_ids = request.env['organisation.coaches'].search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            domain.append(('id', 'in', coach_ids.group_ids.ids))
        if request.env.user.has_group('organisation.group_organisation_athletes'):
            athlete_ids = request.env['organisation.athletes'].search([('partner_id', '=', request.env.user.partner_id.id)])
            domain.append(('athlete_ids', 'in', athlete_ids.ids))
        elif request.env.user.has_group('organisation.group_organisation_parents'):
            athletes = request.env['organisation.parents'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)]).mapped('athlete_ids')
            print(athletes, "athltes")
            domain.append(('athlete_ids', 'in', athletes.ids))
        # if request.env.user.has_group(
        #         'organisation.group_organisation_athletes'):
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        print(org_domain)
        athletes = request.env['organisation.athletes'].sudo().search([])
        organisation = None
        if org_domain:
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1)
            print(organisation)
            if organisation:
                domain.append(('organisation_ids', 'in', [organisation.id]))
                athletes = athletes.filtered(lambda x:x.organisation_ids.ids in [organisation.id])
        print(athletes, "domain")
        groups = request.env['athlete.groups'].sudo().search(domain)
        total = len(groups)
        pager = request.website.pager(
            url='/my/groups',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        groups = groups[offset: offset + 5]
        print(groups, "pager")
        return request.render('sports_erp_dashboard.groups_template',
                              {
                                  'search': search,
                                  'groups': groups,
                                  'total_groups': groups,
                                  'pager': pager,
                                  'is_account': True,
                                  'athletes': athletes,
                                  'total': len(groups),
                                  'filtered_tags': request.env[
                                      'group.tags'].sudo().browse(tag_ids),
                                  'subscriptions': request.env['product.product'].sudo().search([
                                      ('organisation_ids', 'in',
                                       [organisation.id]),
                                      ('company_id', '=',
                                       request.env.user.company_id.id)]),
                                'booking_types': request.env['booking.type'].sudo().search([]),
                                'channels': request.env['chat.hub'].sudo().search([]),
                              })

    @http.route('/create/group', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def create_group(self, **post):
        if post:
            print(post, "post....")
            tag_ids = list(
                map(int, request.httprequest.form.getlist('tags')))
            organisation_ids = list(
                map(int, request.httprequest.form.getlist('organisations')))
            athlete_ids = list(
                map(int, request.httprequest.form.getlist('athletes')))
            document_ids = list(
                map(int, request.httprequest.form.getlist('documents')))
            partner = request.env['res.partner'].sudo().create({
                'name': post.get('name'),
                'last_name': post.get('last_name'),
                'email': post.get('email'),
                'phone': post.get('phone')
            })
            org_domain = []
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
            if request.httprequest.cookies.get(
                    'select_organisation') is not None:
                org_domain.append(('id', '=',
                                   request.httprequest.cookies.get(
                                       'select_organisation')))
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1)
            organisation_ids.append(organisation.id)
            values = {
                'partner_id': partner.id,
                'phone': post.get('phone'),
                'email': post.get('email'),
                'responsible_user_id': int(post.get('responsible_user')) if post.get('responsible_user') else None,
                'tag_ids': [(4, tag) for tag in tag_ids],
                'organisation_ids': [(4, org) for org in organisation_ids],
                'athlete_ids': [(4, athlete) for athlete in athlete_ids],
                'document_ids': [(4, document) for document in document_ids],
            }
            group = request.env['athlete.groups'].sudo().create(values)

            return request.redirect('/my/groups')

    @http.route('/remove/group/<model("athlete.groups"):group_id>',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_group(self, group_id=None):
        if group_id:
            group_id.sudo().unlink()
        return request.redirect('/my/groups')

    @http.route('/group/<model("athlete.groups"):group_id>',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def group_details(self, group_id=None):
        values = {
            'group': group_id,
            'is_account': True
        }
        return request.render(
            'sports_erp_dashboard.group_dashboard_details_template', values)

    @http.route('/update/group',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def update_group(self, **post):
        print(post, "post")
        values = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone')
        }
        print(post.get('group'))
        group = request.env['athlete.groups'].sudo().browse(
            int(post.get('group')))
        group.sudo().write(values)
        return request.redirect('/group/%s' % group.id)

    @http.route(['/my/disciplines', '/my/disciplines/page/<int:page>'],
                type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def my_disciplines(self, page=0, search='', **post):
        print("self....", search)
        tag_ids = list(
            map(int, request.httprequest.form.getlist('filtered_tags')))
        domain = []
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        if tag_ids:
            domain.append(('tag_ids', 'in', tag_ids))
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))
        disciplines = request.env['organisation.discipline'].sudo().search(
            domain)
        total = len(disciplines)
        pager = request.website.pager(
            url='/my/disciplines',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        disciplines = disciplines[offset: offset + 5]
        return request.render('sports_erp_dashboard.discipline_template',
                              {
                                  'search': search,
                                  'total_disciplines': disciplines,
                                  'disciplines': disciplines,
                                  'organisations': request.env['organisation.organisation'].sudo().search(
                                      [('allowed_user_ids', 'in', [request.env.user.id])]),
                                  'pager': pager,
                                  'is_account': True,
                                  'total': total,
                                  'filtered_tags': request.env[
                                      'discipline.tags'].sudo().browse(tag_ids),
                              })

    @http.route(['/my/discipline_details/<int:discipline_id>'], type='http',
                auth='user', website=True)
    def discipline_details(self, **kwargs):
        discipline = request.env['organisation.discipline'].sudo().browse(
            kwargs.get('discipline_id'))
        return request.render(
            'sports_erp_dashboard.discipline_details_template',
            {'is_account': True,
             'discipline': discipline,
             'res_users': request.env[
                 'res.users'].sudo().search([]),
             'tags': request.env['venues.tags'].sudo().search(
                 [
                     ('id', 'not in', discipline.tag_ids.ids)
                 ]),
             'organisations': request.env[
                 'organisation.organisation'].sudo().search([
                 ('id', 'not in', discipline.organisation_ids.ids)
             ])
             })

    @http.route(['/create/discipline'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def create_discipline(self, **post):
        if post:
            tag_ids = list(
                map(int, request.httprequest.form.getlist('tags')))
            organisation_ids = list(
                map(int, request.httprequest.form.getlist('organisations')))

            partner = request.env['res.partner'].sudo().create({
                'name': post.get('name'),
            })
            org_domain = []
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
            if request.httprequest.cookies.get(
                    'select_organisation') is not None:
                org_domain.append(('id', '=',
                                   request.httprequest.cookies.get(
                                       'select_organisation')))
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1)
            organisation_ids.append(organisation.id)
            # user = request.env['res.users'].sudo().create({
            #     'name': post.get('name'),
            #     'login': post.get('email'),
            #     'partner_id': partner.id,
            # })
            values = {
                'partner_id': partner.id,
                # 'phone': post.get('phone'),
                # 'email': post.get('email'),
                'tag_ids': [(4, tag) for tag in tag_ids],
                'organisation_ids': [(4, org) for org in organisation_ids],
            }
            request.env['organisation.discipline'].sudo().create(values)
            return request.redirect('/my/disciplines')

    @http.route(['/remove/discipline/<int:discipline_id>'], type='http',
                auth='user', csrf=False, website=True)
    def delete_discipline(self, **post):
        request.env['organisation.discipline'].sudo().browse(
            int(post.get('discipline_id'))).unlink()
        return request.redirect('/my/disciplines')

    @http.route(['/my/update_discipline'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def update_discipline(self, **post):
        discipline = request.env[
            'organisation.discipline'].sudo().browse(
            int(post.get('discipline_id')))
        discipline.sudo().write({
            'name': post.get('name'),
        })
        discipline.sudo().partner_id.write({
            'name': post.get('name'),
        })
        discipline.sudo().write({
            'tag_ids': [(5, 0, 0)],
            'organisation_ids': [(5, 0, 0)]
        })
        tag_ids = list(
            map(int, request.httprequest.form.getlist('tags')))
        if tag_ids:
            discipline.sudo().write({
                'tag_ids': [(4, tag) for tag in tag_ids]
            })
        org_ids = list(
            map(int, request.httprequest.form.getlist('organisation')))
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        org_ids.append(organisation.id)
        if org_ids:
            discipline.sudo().write({
                'organisation_ids': [(4, org) for org in org_ids]
            })
        return request.redirect('/my/discipline_details/%s' % discipline.id)

    @http.route(['/my/venues', '/my/venues/page/<int:page>'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def my_venues(self, page=0, search='', **post):
        state_ids = list(
            map(int, request.httprequest.form.getlist('state_ids')))
        tag_ids = list(
            map(int, request.httprequest.form.getlist('filtered_tags')))
        domain = []
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))
        if post.get('city'):
            domain.append(('partner_id.city', 'ilike', post.get('city')))
        if state_ids:
            domain.append(('partner_id.state_id', 'in', state_ids))
        if tag_ids:
            domain.append(('tag_ids', 'in', tag_ids))

        venues = request.env['organisation.venues'].sudo().search(domain)
        total = len(venues)
        pager = request.website.pager(
            url='/my/venues',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        venues = venues[offset: offset + 6]
        values = {
            'search': search,
            'venues': venues,
            'pager': pager,
            'is_account': True,
            'total_venues': venues,
            'organisations': request.env[
            'organisation.organisation'].sudo().search([('allowed_user_ids', 'in', [request.env.user.id])]),
            'countries': request.env[
                'res.country'].sudo().search([]),
            'states': request.env[
                'res.country.state'].sudo().search([]),
            'total': total,
            'filtered_states': request.env[
                'res.country.state'].sudo().browse(
                state_ids) if state_ids else None,
            'filtered_city': post.get('city') if post.get('city') else None,
            'filtered_tags': request.env[
                'venues.tags'].sudo().browse(tag_ids)
        }
        return request.render('sports_erp_dashboard.venues_template',
                              values)

    @http.route(['/my/venue_details/<int:venue_id>'], type='http',
                auth='user', website=True)
    def venue_details(self, **kwargs):
        venue = request.env['organisation.venues'].sudo().browse(
            kwargs.get('venue_id'))
        return request.render('sports_erp_dashboard.venue_details_template',
                              {'is_account': True,
                               'venue': venue,
                               'res_users': request.env[
                                   'res.users'].sudo().search([]),
                               'tags': request.env['venues.tags'].sudo().search(
                                   [
                                       ('id', 'not in', venue.tag_ids.ids)
                                   ]),
                               'organisations': request.env['organisation.organisation'].sudo().search([('allowed_user_ids', 'in', [request.env.user.id])]),
                               'states': request.env[
                                   'res.country.state'].sudo().search([
                                   ('id', '!=', venue.partner_id.state_id.id)
                               ]),
                               'countries': request.env[
                                   'res.country'].sudo().search([
                                   ('id', '!=', venue.partner_id.country_id.id)
                               ]),
                               })

    @http.route(['/create/venue'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def create_venue(self, **post):
        if post:
            venue_partner = request.env['res.partner'].sudo().create({
                'name': post.get('venue_name'),
                'phone': post.get('phone'),
                'street': post.get('street_name'),
                'city': post.get('city_name'),
                'state_id': int(post.get('state_id')),
                'zip': post.get('zip_code'),
                'country_id': int(post.get('country_id'))
            })
            print('venue', venue_partner)
            org_domain = []
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
            if request.httprequest.cookies.get(
                    'select_organisation') is not None:
                org_domain.append(('id', '=',
                                   request.httprequest.cookies.get(
                                       'select_organisation')))
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1)
            tag_ids = list(
                map(int, request.httprequest.form.getlist('tags')))
            organisation_ids = list(
                map(int, request.httprequest.form.getlist('organisations')))
            organisation_ids.append(organisation.id)
            values = {
                'partner_id': venue_partner.id,
                'phone': post.get('phone'),
                'responsible_user_id': int(post.get('responsible_user'))
                if post.get('responsible_user') else None,
                'tag_ids': [(4, tag) for tag in tag_ids],
                'organisation_ids': [(4, org) for org in organisation_ids],
            }
            request.env['organisation.venues'].sudo().create(values)
            return request.redirect('/my/venues')

    @http.route(['/my/delete_venue/<int:venue_id>'], type='http',
                auth='user', csrf=False, website=True)
    def delete_venue(self, **post):
        request.env['organisation.venues'].sudo().browse(
            int(post.get('venue_id'))).unlink()
        return request.redirect('/my/venues')

    @http.route(['/my/update_venues'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def update_venue(self, **post):
        venue = request.env[
            'organisation.venues'].sudo().browse(int(post.get('venue_id')))
        venue.sudo().write({
            'name': post.get('name'),
            'phone': post.get('phone'),
            'date': post.get('date'),
            'email': post.get('email'),
            'responsible_user_id': int(
                post.get('responsible_user')) if post.get(
                'responsible_user') else None,
        })
        venue.sudo().partner_id.write({
            'name': post.get('name'),
            'phone': post.get('phone'),
            'email': post.get('email'),
            'street': post.get('street_name'),
            'city': post.get('city_name'),
            'state_id': int(post.get('state_id')),
            'zip': post.get('zip_code'),
            'country_id': int(post.get('country_id')),
        })
        venue.sudo().write({
            'tag_ids': [(5, 0, 0)],
            'organisation_ids': [(5, 0, 0)]
        })
        tag_ids = list(
            map(int, request.httprequest.form.getlist('tags')))
        if tag_ids:
            venue.sudo().write({
                'tag_ids': [(4, tag) for tag in tag_ids]
            })
        org_ids = list(
            map(int, request.httprequest.form.getlist('organisation')))
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        if organisation:
            org_ids.append(organisation.id)
        if org_ids:
            venue.sudo().write({
                'organisation_ids': [(4, org) for org in org_ids]
            })
        return request.redirect('/my/venue_details/%s' % venue.id)

    #Fans
    @http.route(['/my/fans', '/my/fans/page/<int:page>'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def fans(self, page=0, search='', **post):
        tag_ids = list(
            map(int, request.httprequest.form.getlist('filtered_tags')))
        domain = []
        org_domain = []
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        if tag_ids:
            domain.append(('tag_ids', 'in', tag_ids))
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
              request.httprequest.cookies.get('select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(org_domain, limit=1)
        if organisation:
            domain.append(('organisation_id', 'in', [organisation.id]))
        fans = request.env['organisation.fans'].sudo().search(domain)
        total = len(fans)
        pager = request.website.pager(
            url='/my/fans',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        fans = fans[offset: offset + 6]
        values = {
            'search': search,
            'fans': fans,
            'pager': pager,
            'is_account': True,
            'total_fans': fans,
            'total': total,
            'subscriptions': request.env['product.product'].sudo().search([
                                      ('organisation_ids', 'in',
                                       [organisation.id]),
                                      ('company_id', '=',
                                       request.env.user.company_id.id)]),
            'booking_types': request.env['booking.type'].sudo().search([]),
            'channels': request.env['chat.hub'].sudo().search([]),
        }
        return request.render('sports_erp_dashboard.fans_template',
                              values)

    @http.route(['/create/fan'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def create_fan(self, **post):
        if post:
            fan_partner = request.env['res.partner'].sudo().create({
                'name': post.get('fan_name'),
                'last_name': post.get('last_name'),
                'email': post.get('email'),
                'phone': post.get('phone')
            })
            tag_ids = list(
                map(int, request.httprequest.form.getlist('tags')))
            organisation = post.get('organisation')
            if not post.get('organisation'):
                organisation = request.env['organisation.organisation'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)]).id
            values = {
                'partner_id': fan_partner.id,
                'phone': post.get('phone'),
                'email': post.get('email'),
                'organisation_id': organisation,
                'tag_ids': [(4, tag) for tag in tag_ids],
            }
            request.env['organisation.fans'].sudo().create(values)
            fan_partner.write({
                'create_booking': True if post.get(
                    'booking') == 'on' else False
            })
            return request.redirect('/my/fans')

    @http.route(['/my/delete_fan/<int:fan_id>'], type='http',
                auth='user', csrf=False, website=True)
    def delete_fan(self, **post):
        request.env['organisation.fans'].sudo().browse(
            int(post.get('fan_id'))).unlink()
        return request.redirect('/my/fans')

    @http.route(['/my/fan_details/<int:fan_id>'], type='http',
                auth='user', website=True)
    def fan_details(self, **kwargs):
        fan = request.env['organisation.fans'].sudo().browse(
            kwargs.get('fan_id'))
        return request.render('sports_erp_dashboard.fan_details_template',
                              {'is_account': True,
                               'fan': fan,
                               'res_users': request.env[
                                   'res.users'].sudo().search([]),
                               'tags': request.env['fans.tags'].sudo().search(
                                   [('id', 'not in', fan.tag_ids.ids)]),
                               'organisations': request.env[
                                   'organisation.organisation'].sudo().search(
                                   [('id', '!=', fan.organisation_id.id),
                                    ('allowed_user_ids', 'in', [request.env.user.id])]),
                               })

    @http.route(['/my/update_fan'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def update_fan(self, **post):
        print("post", post)
        fan = request.env[
            'organisation.fans'].sudo().browse(int(post.get('fan_id')))
        fan.sudo().write({
            'name': post.get('name'),
            'phone': post.get('phone'),
            'email': post.get('email'),
            'organisation_id': int(
                post.get('organisation')) if post.get(
                'organisation') else None,
        })
        fan.sudo().partner_id.write({
            'name': post.get('name'),
            'phone': post.get('phone'),
            'email': post.get('email'),
        })
        fan.sudo().write({
            'tag_ids': [(5, 0, 0)],
        })
        tag_ids = list(
            map(int, request.httprequest.form.getlist('tags')))
        if tag_ids:
            fan.sudo().write({
                'tag_ids': [(4, tag) for tag in tag_ids]
            })
        return request.redirect('/my/fan_details/%s' % fan.id)



    # Chathub
    @http.route('/create/chathub', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def create_chathub(self, **post):
        print(post, "posttttt")
        if post:
            member_ids = list(
                map(int, request.httprequest.form.getlist('members')))
            member_ids.append(request.env.user.partner_id.id)
            values = {
                'name': post.get('name'),
                'partner_ids': [(4, member) for member in member_ids],
                'description': post.get('description')
            }
            request.env['chat.hub'].sudo().create(values)
            return request.redirect('/edit/chathubs')

    @http.route('/edit/chathubs', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def edit_chathub(self, search='', page=0, **post):
        if request.env.user._is_public():
            return request.redirect('/web/login')
        domain = []
        org_domain = []
        if request.env.user.has_group('organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        elif request.env.user.has_group('organisation.group_organisation_coaches'):
            coaches = request.env['organisation.coaches'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)])
            org_domain.append(('id', 'in', coaches.organisation_ids))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        domain.append(('partner_ids', 'in', [request.env.user.partner_id.id]))
        chat_hubs = request.env['chat.hub'].sudo().search(domain)
        total = len(chat_hubs)
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        members = request.env['res.partner'].sudo().search(
            [('id', '!=', organisation.partner_id.id),
             ('organisation_ids', 'in', [organisation.id]),
             ('company_id', '=', request.env.user.company_id.id)])
        pager = request.website.pager(
            url='/edit/chathubs',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        chat_hubs = chat_hubs[offset: offset + 6]
        values = {
            'search': search,
            'chat_hubs': chat_hubs,
            'pager': pager,
            'is_account': True,
            'members': members,
            'total': total}
        return request.render('sports_erp_dashboard.chat_hub_template', values)

    @http.route('/my/chat_hub_details/<model("chat.hub"):chathub_id>',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def chathub_details(self, chathub_id=None):
        print("chathub", chathub_id.read())
        print("chathub", chathub_id.partner_ids)

        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        members = request.env['res.partner'].sudo().search(
            [('id', '!=', organisation.partner_id.id),
             ('organisation_ids', 'in', [organisation.id]),
             ('company_id', '=', request.env.user.company_id.id)])
        return request.render('sports_erp_dashboard.chathub_details_template',
                              {'is_account': True,
                               'chathub': chathub_id,
                               'members': members

                               # 'res_users': request.env[
                               #     'res.users'].sudo().search([]),
                               # 'tags': request.env['fans.tags'].sudo().search(
                               #     [('id', 'not in', fan.tag_ids.ids)]),
                               # 'organisations': request.env[
                               #     'organisation.organisation'].sudo().search(
                               #     [('id', '!=', fan.organisation_id.id)]),
                               })

    @http.route('/my/delete_chat_hub/<model("chat.hub"):chathub_id>',
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def remove_chathub(self, chathub_id=None):
        if chathub_id:
            chathub_id.sudo().unlink()
        return request.redirect('/edit/chathubs')

    @http.route(['/my/update_chathub'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def update_chathub(self, **post):
        print("post", post)
        chathub = request.env[
            'chat.hub'].sudo().browse(int(post.get('chathub_id')))
        chathub.sudo().write({
            'name': post.get('name'),
            'description': post.get('description'),
        })
        chathub.sudo().write({
            'partner_ids': [(5, 0, 0)],
        })
        member_ids = list(
            map(int, request.httprequest.form.getlist('members')))
        print(member_ids)
        chathub.sudo().write({
            'partner_ids': [(4, member) for member in member_ids]
        })
        print(chathub.read())
        return request.redirect('/my/chat_hub_details/%s' % chathub.id)
