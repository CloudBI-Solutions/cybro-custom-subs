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
from dateutil.relativedelta import relativedelta


class Subscriptions(CustomerPortal):
    @http.route(['/subscriptions', '/subscriptions/page/<int:page>', '/subscriptions', '/subscriptions/page/<int:page>'], type='http', auth="public", website=True)
    def subscriptions(self, page=1, search=''):
        Subscription = request.env['product.template'].sudo().search([])
        print(Subscription, "subscriptions")
        domain = [('activate_subscription', '=', True), ('is_able_to_assign', '=', True), ('is_published', '=', True)]

        if search:
            domain.append(('name', 'ilike', search))
        subscriptions = Subscription.sudo().search(domain)
        return request.render('sports_erp_dashboard.subscription_home_template', {'subscription': subscriptions})
    #     Subscription = request.env['product.template']
    #     # SudoEventType = request.env['event.type'].sudo()
    #
    #     # searches.setdefault('search', '')
    #     # searches.setdefault('date', 'all')
    #     # searches.setdefault('tags', '')
    #     # searches.setdefault('type', 'all')
    #     # searches.setdefault('country', 'all')
    #
    #     website = request.website
    #
    #     step = 12  # Number of events per page
    #
    #     # options = {
    #     #     'displayDescription': False,
    #     #     'displayDetail': False,
    #     #     'displayExtraDetail': False,
    #     #     'displayExtraLink': False,
    #     #     'displayImage': False,
    #     #     'allowFuzzy': not searches.get('noFuzzy'),
    #     #     'date': searches.get('date'),
    #     #     'tags': searches.get('tags'),
    #     #     'type': searches.get('type'),
    #     #     'country': searches.get('country'),
    #     # }
    #     order = 'date_begin'
    #     if searches.get('date', 'all') == 'old':
    #         order = 'date_begin desc'
    #     order = 'is_published desc, ' + order
    #     search = searches.get('search')
    #     event_count, details, fuzzy_search_term = website._search_with_fuzzy("events", search,
    #         limit=page * step, order=order, options=options)
    #     event_details = details[0]
    #     events = event_details.get('results', Event)
    #     events = events[(page - 1) * step:page * step]
    #
    #     # count by domains without self search
    #     domain_search = [('name', 'ilike', fuzzy_search_term or searches['search'])] if searches['search'] else []
    #
    #     no_date_domain = event_details['no_date_domain']
    #     dates = event_details['dates']
    #     for date in dates:
    #         if date[0] != 'old':
    #             date[3] = Event.search_count(expression.AND(no_date_domain) + domain_search + date[2])
    #
    #     no_country_domain = event_details['no_country_domain']
    #     countries = Event.read_group(expression.AND(no_country_domain) + domain_search, ["id", "country_id"],
    #         groupby="country_id", orderby="country_id")
    #     countries.insert(0, {
    #         'country_id_count': sum([int(country['country_id_count']) for country in countries]),
    #         'country_id': ("all", _("All Countries"))
    #     })
    #
    #     search_tags = event_details['search_tags']
    #     current_date = event_details['current_date']
    #     current_type = None
    #     current_country = None
    #
    #     if searches["type"] != 'all':
    #         current_type = SudoEventType.browse(int(searches['type']))
    #
    #     if searches["country"] != 'all' and searches["country"] != 'online':
    #         current_country = request.env['res.country'].browse(int(searches['country']))
    #
    #     pager = website.pager(
    #         url="/event",
    #         url_args=searches,
    #         total=event_count,
    #         page=page,
    #         step=step,
    #         scope=5)
    #
    #     keep = QueryURL('/event', **{key: value for key, value in searches.items() if (key == 'search' or value != 'all')})
    #
    #     searches['search'] = fuzzy_search_term or search
    #
    #     values = {
    #         'current_date': current_date,
    #         'current_country': current_country,
    #         'current_type': current_type,
    #         'event_ids': events,  # event_ids used in website_event_track so we keep name as it is
    #         'dates': dates,
    #         'categories': request.env['event.tag.category'].search([('is_published', '=', True)]),
    #         'countries': countries,
    #         'pager': pager,
    #         'searches': searches,
    #         'search_tags': search_tags,
    #         'keep': keep,
    #         'search_count': event_count,
    #         'original_search': fuzzy_search_term and search,
    #     }
    #
    #     if searches['date'] == 'old':
    #         # the only way to display this content is to set date=old so it must be canonical
    #         values['canonical_params'] = OrderedMultiDict([('date', 'old')])
    #
    #     return request.render("sports_erp_dashboard.index", values)

    # @http.route(['/subscriptions'], type='http',
    #             auth='user', website=True)
    # def subscriptions(self, page=0, search='', **post):
    #     print("Subscriptions")
    #     return request.redirect('/event')

    # Subscription
    @http.route(['/my/subscriptions', '/my/subscriptions/page/<int:page>'], type='http',
                auth='user', website=True)
    def subscription_home(self, page=0, search='', **post):
        domain = []
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
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        domain.append(('company_id', '=', request.env.user.company_id.id))
        subscription = request.env['subscription.subscription'].sudo().search(
            domain)
        customers = request.env['res.partner'].sudo().search(
            [('id', '!=', organisation.partner_id.id),
             ('organisation_ids', 'in', [organisation.id]),
             ('company_id', '=', request.env.user.company_id.id)])
        contracts = request.env['subscription.contract'].sudo().search([
            ('organisation_ids', 'in', [organisation.id]),
            ('company_id', '=', request.env.user.company_id.id)])
        products = request.env['product.product'].sudo().search([
            ('organisation_ids', 'in', [organisation.id]),
            ('company_id', '=', request.env.user.company_id.id)])
        plans = request.env['subscription.plan'].sudo().search([
            ('organisation_ids', 'in', [organisation.id]),
            ('company_id', '=', request.env.user.company_id.id)])
        total = len(subscription)
        pager = request.website.pager(
            url='/my/subscriptions',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        subscription = subscription[offset: offset + 6]
        values = {
            'search': search,
            'subscriptions': subscription,
            'pager': pager,
            'is_account': True,
            'total_subscriptions': request.env[
                'subscription.subscription'].sudo().search(
                []),
            'customers': customers,
            'contracts': contracts,
            'products': products,
            'plans': plans,
            'total': total,
        }
        print(customers, "customers")
        return request.render(
            'sports_erp_dashboard.subscription_template', values)

    @http.route('/my/update_subscription', type='http', auth='user',
                website=True, methods=['POST', 'GET'])
    def update_subscription(self, **post):
        tax_id = list(
            map(int, request.httprequest.form.getlist('taxes')))
        next_payment = post.get('next_payment').replace("T", " ")
        print('nex', post)
        subscription = request.env['subscription.subscription'].browse(
            int(post.get('subscription_id'))
        )
        values = {
            'active': True if post.get(
                'active_subscription') == 'on' else False,
            'contract_id': int(post.get('contract')),
            'customer_name': int(post.get('customer')),
            'customer_billing_address': int(post.get('billing_address')),
            'company_id': int(post.get('company_id')),
            'product_id': int(post.get('product')),
            'quantity': float(post.get('quantity')),
            'sub_plan_id': int(post.get('plan')),
            'duration': int(post.get('duration')),
            'unit': post.get('duration_type'),
            'trial_period': True if post.get(
                'has_trial') == 'on' else False,
            'trial_duration': int(post.get('trial_duration')),
            'trial_duration_unit': post.get('trial_duration_type'),
            'price': float(post.get('price')),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date') if post.get(
                'end_date') else None,
            'num_billing_cycle': int(post.get('num_billing_cycle')),
            'source': post.get('source'),
            'so_origin': int(post.get('so_origin')) if post.get(
                'so_origin') else None,
            'subscription_ref': post.get('ref'),
            'project_id': int(post.get('project')) if post.get(
                'project') else None,
            'next_payment_date': next_payment,
        }
        subscription.sudo().write(values)
        subscription.sudo().write({
            'tax_id': [(5, 0, 0)],
        })
        if tax_id:
            subscription.sudo().write({
                'tax_id': [(4, tax) for tax in tax_id]
            })
        if int(post.get('state_subscription')):
            print(int(post.get('state_subscription')), "post")
            if int(post.get('state_subscription')) == request.env.ref(
                    'subscription_management.stage_active').id:
                subscription.get_confirm_subscription()
            if int(post.get('state_subscription')) == request.env.ref(
                    'subscription_management.stage_frozen').id:
                subscription.get_frozen_subscription()
            if int(post.get('state_subscription')) == request.env.ref(
                    'subscription_management.stage_doubtful').id:
                subscription.get_doubtful_subscription()
            if int(post.get('state_subscription')) == request.env.ref(
                    'subscription_management.stage_not_renewing').id:
                subscription.get_not_renewing_subscription()
            if int(post.get('state_subscription')) == request.env.ref(
                    'subscription_management.stage_terminated').id:
                subscription.get_terminated_subscription()

        return request.redirect('/my/subscription_details/%s' % subscription.id)

    @http.route('/my/subscription_details/<int:subscription_id>',
                type='http',
                auth='user', website=True)
    def subscription_details(self, **kwargs):
        print('kwar', kwargs)
        subscription = request.env[
            'subscription.subscription'].sudo().browse(kwargs.get('subscription_id'))
        print("subs", subscription.next_payment_date)
        values = {
            'subscription': subscription,
            'is_account': True,
            'stages': request.env['subscription.stage'].sudo().search([
                ('id', '!=', subscription.stage_id.id)
            ]),
            'contracts': request.env['subscription.contract'].sudo().search([
                ('id', '!=', subscription.contract_id.id)
            ]),
            'customers': request.env['res.partner'].sudo().search([
                ('id', '!=', subscription.customer_name.id)
            ]),
            'billing_address': request.env['res.partner'].sudo().search([
                ('id', '!=', subscription.customer_billing_address.id)
            ]),
            'products': request.env['product.product'].sudo().search([
                ('id', '!=', subscription.product_id.id),
                ('sale_ok', '=', True),
                ('activate_subscription', '=', True)
            ]),
            'taxes': request.env['account.tax'].sudo().search([
                ('id', 'not in', subscription.tax_id.ids)]),
            'plans': request.env['subscription.plan'].sudo().search([
                ('id', '!=', subscription.sub_plan_id.id)
            ]),
            'sos': request.env['sale.order'].sudo().search([
                ('id', '!=', subscription.so_origin.id)
            ]),
            'projects': request.env['project.project'].sudo().search([
                ('id', '!=', subscription.project_id.id)
            ]),
        }
        return request.render(
            'sports_erp_dashboard.subscription_details', values)



    @http.route(['/create/subscription'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def create_subscription(self, **post):
        tax_ids = list(
            map(int, request.httprequest.form.getlist('subscription_taxes')))
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        customer_ids = list(
            map(int, request.httprequest.form.getlist('subscription_customers')))
        product = request.env['product.product'].sudo().search([('id', '=', int(post.get('subscription_products')))])
        for rec in customer_ids:
            values = {
                'active': True if post.get(
                    'active_subscription') == 'on' else False,
                'contract_id': product.subscription_contract_id.id,
                'customer_name': rec,
                'customer_billing_address': rec,
                'company_id': request.env.user.company_id.id,
                'product_id': int(post.get('subscription_products')),
                'tax_id': [(4, tax) for tax in tax_ids],
                'quantity': float(post.get('quantity')),
                'sub_plan_id': product.subscription_plan_id.id,
                'price': product.subscription_plan_id.plan_amount if product.subscription_plan_id.override_product_price else product.lst_price,
                'duration': product.subscription_plan_id.duration,
                'unit': product.subscription_plan_id.unit,
                'start_date': post.get('start_date') if post.get('start_date') else False ,
                'end_date': post.get('end_date') if post.get('end_date') else False,
                # 'num_billing_cycle': int(post.get('billing_cycle')),
                # 'source': post.get('source'),
                # 'subscription_ref': post.get('subscription_ref'),
                # 'project_id': int(post.get('project_id')),
                # 'next_payment_date': post.get('next_payment') if post.get('next_payment') else False,

            }
            if post.get('has_trial_period') == 'on':
                values.update({
                    'trial_period': True,
                    'trial_duration': int(post.get('trial_duration')),
                    'trial_duration_unit': post.get('trial_duration_type')
                })

            if organisation:
                values['organisation_ids'] = [
                    (4, organisation.id if organisation else False)]
            subscription = request.env['subscription.subscription'].sudo().create(
                values)
            if post.get('activate') == 'on':
                subscription.get_confirm_subscription()
        return request.redirect('/my/subscriptions')

    # Contracts

    @http.route(['/my/update_subscription_contract'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def subscription_contract_update(self, **post):
        subscription_contract = request.env['subscription.contract'].sudo().browse(
            int(post.get('subscription_contract_id')))
        values = {
            'name': post.get('name'),
            'partner_id': int(post.get('customer_id')) if post.get(
                'customer_id') else None,
            'pricelist_id': int(post.get('pricelist_id')) if post.get(
                'pricelist_id') else None,
            'contract_status': post.get('contract_status'),
            'reason': post.get('reason'),
            'latest_record': True if post.get(
                'latest_record') == 'on' else False,
            'contract_type': post.get('contract_type'),
            'allowed_freeze_count': int(post.get('allowed_freeze_count'))
            if post.get('allowed_freeze_count') else None,
            'freeze_price': float(post.get('freeze_price'))
            if post.get('freeze_price') else None,
            'freeze_period': int(post.get('freeze_period'))
            if post.get('freeze_period') else None,
        }
        subscription_contract.sudo().write(values)
        if post.get('signed_agreement'):
            subscription_contract.write({
                'signed_agreement': base64.b64encode(post.get(
                    'signed_agreement').read()),
            })
        return request.redirect(
            '/my/subscription_contract_details/%s' % subscription_contract.id)

    @http.route(['/my/subscription_contract_details/<int:contract_id>'],
                type='http',
                auth='user', website=True)
    def subscription_contract_details(self, **kwargs):
        subscription_contract = request.env[
            'subscription.contract'].sudo().browse(
            kwargs.get('contract_id'))
        print(subscription_contract.latest_record)
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        customers = request.env['res.partner'].sudo().search(
            [('id', '!=', organisation.partner_id.id),
             ('organisation_ids', 'in', [organisation.id]),
             ('company_id', '=', request.env.user.company_id.id)])
        values = {
            'is_account': True,
            'subscription_contract': subscription_contract,
            'customers':customers,
            'price_lists': request.env['product.pricelist'].search([
                ('id', '!=', subscription_contract.pricelist_id.id)
            ]),
        }
        return request.render(
            'sports_erp_dashboard.subscription_contract_edit_template', values)

    @http.route('/my/delete_subscription_contract/<int:subscription_contract>',
                type='http', auth='user', website=True
                )
    def delete_subscription_contract(self, **kwargs):
        subscription_contract = request.env[
            'subscription.contract'].sudo().browse(
            kwargs.get('subscription_contract'))
        subscription_contract.sudo().unlink()
        return request.redirect('/my/subscription_contracts')

    @http.route(['/create/subscription_contract'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def create_contract(self, **post):
        customers = list(
            map(int, request.httprequest.form.getlist('customers')))
        print(customers)
        # values['customer_ids'] = [(4, customer) for customer in customers],
        values = {
            'name': post.get('contract_name'),
            'partner_id': int(post.get('partner_id')) if post.get('partner_id') else None,
            'pricelist_id': int(post.get('pricelist')) if post.get('pricelist') else None,
            'contract_status': post.get('active'),
            'reason': post.get('reason'),
            'latest_record': True if post.get(
                'latest_record') == 'on' else False,
            'contract_type': post.get('contract_type'),
            'allowed_freeze_count': post.get('allowed_freeze_count'),
            'freeze_period': post.get('freeze_period'),
            'freeze_price': post.get('freeze_price'),
            'company_id': request.env.user.company_id.id,
            'customer_ids': [(4, customer) for customer in customers]
        }
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        if organisation:
            values['organisation_ids'] = [
                (4, organisation.id if organisation else False)]

        print(values)
        subscription_contract = request.env[
            'subscription.contract'].sudo().create(
            values)
        if post.get('signed_agreement'):
            subscription_contract.sudo().write({
                'signed_agreement': base64.b64encode(post.get(
                    'signed_agreement').read())
            })
        return request.redirect('/my/subscription_contracts')

    @http.route(['/my/subscription_contracts',
                 '/my/subscription_contracts/page/<int:page>'], type='http',
                auth='user', website=True)
    def contracts_home(self, page=0, search='', **post):
        domain = [('company_id', '=', request.env.user.company_id.id), ]
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
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        subscription_contract = request.env[
            'subscription.contract'].sudo().search(
            domain)
        total = len(subscription_contract)
        pager = request.website.pager(
            url='/my/subscription_contracts',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        subscription_contract = subscription_contract[offset: offset + 6]
        print(subscription_contract)
        customers = request.env['res.partner'].sudo().search(
            [('id', '!=', organisation.partner_id.id),
             ('organisation_ids', 'in', [organisation.id]),
             ('company_id', '=', request.env.user.company_id.id)])
        values = {
            'search': search,
            'subscription_contract': subscription_contract,
            'pager': pager,
            'is_account': True,
            'customers': customers,
            'total_subscription_contracts': request.env[
                'subscription.contract'].sudo().search(
                [('company_id', '=', request.env.user.company_id.id,
                  )]),
            'total': total,
        }
        return request.render(
            'sports_erp_dashboard.subscription_contract_template', values)

    # Subscription Products

    @http.route(['/my/subscription_products', '/my/subscription_products/page/<int:page>'], type='http',
                auth='user', website=True)
    def products_home(self, page=0, search='', **post):
        domain = [('company_id', '=', request.env.user.company_id.id), ]
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        print("dom", domain)

        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env[
            'organisation.organisation'].sudo().search(
            org_domain, limit=1)
        print(organisation)
        if organisation:
            domain.append(('organisation_ids', 'in', [organisation.id]))
        subscription_products = request.env[
            'product.product'].sudo().search(
            domain)
        total = len(subscription_products)
        pager = request.website.pager(
            url='/my/subscription_products',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        subscription_product = subscription_products[offset: offset + 6]
        contracts = request.env['subscription.contract'].sudo().search([
            ('organisation_ids', 'in', [organisation.id]),
            ('company_id', '=', request.env.user.company_id.id)])
        products = request.env['product.product'].sudo().search([
            ('organisation_ids', 'in', [organisation.id]),
            ('company_id', '=', request.env.user.company_id.id)])
        plans = request.env['subscription.plan'].sudo().search([
            ('organisation_ids', 'in', [organisation.id]),
            ('company_id', '=', request.env.user.company_id.id)])
        values = {
            'search': search,
            'subscription_product': subscription_product,
            'pager': pager,
            'is_account': True,
            'total_subscription_products': products,
            'plans': plans,
            'contracts': contracts,
            'total': total,
        }
        return request.render(
            'sports_erp_dashboard.subscription_product_template', values)

    @http.route('/my/delete_subscription_product/<int:subscription_product>',
                type='http', auth='public', csrf=False, website=True)
    def delete_subscription_product(self, **kwargs):
        subscription_product = request.env['product.product'].sudo().browse(
            kwargs.get('subscription_product'))
        subscription_product.sudo().unlink()
        return request.redirect('/my/subscription_products')

    @http.route(['/create/subscription_product'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def subscription_product(self, **post):
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        values = {'name': post.get('product_name'),
                  'activate_subscription': True,
                  'is_subscription_addon': True if post.get(
                      'is_subscription_addon') == 'on' else False,
                  'detailed_type': 'service',
                  'subscription_plan_id': int(
                      post.get('subscription_plan_ids')),
                  'subscription_contract_id': post.get(
                      'subscription_contract_ids'),
                  'list_price': post.get('sale_price'),
                  'company_id': request.env.user.company_id.id,
                  'is_able_to_assign': True if post.get('is_able_to_assign') == 'on' else False,
                  'is_published': True,
                  'website_published': True
                  # 'organisation_ids': [(4, organisation.id if organisation else False)]
                  }
        if organisation:
            values['organisation_ids'] = [
                (4, organisation.id if organisation else False)]
        subscription_product = request.env[
            'product.product'].sudo().create(
            values)
        if post.get('photo'):
            subscription_product.sudo().write({
                'image_1920': base64.b64encode(post.get(
                    'photo').read())
            })
        return request.redirect('/my/subscription_products')

    @http.route(['/my/subscription_product_details/<int:product_id>'],
                type='http', auth='public', csrf=False, website=True)
    def subscription_product_details(self, **kwargs):
        print("kwa", kwargs)
        subscription_product = request.env['product.product'].sudo().browse(
            kwargs.get('product_id'))
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        values = {
            'subscription_product': subscription_product,
            'is_account': True,
            'contracts': request.env['subscription.contract'].sudo().search([
            ('organisation_ids', 'in', [organisation.id]),
            ('company_id', '=', request.env.user.company_id.id)]),
            'plans': request.env['subscription.plan'].sudo().search([
            ('organisation_ids', 'in', [organisation.id]),
            ('company_id', '=', request.env.user.company_id.id)]),
        }
        print(subscription_product)
        response = request.render(
            "sports_erp_dashboard.subscription_product_details", values)
        return response

    @http.route(['/my/update_subscription_product'], type='http',
                auth='public', csrf=False, website=True,
                methods=['POST', 'GET'])
    def update_subscription_product(self, **post):
        print('post', post)
        product = request.env['product.product'].sudo().browse(
            int(post.get('subscription_product_id')))
        values = {
            'name': post.get('name'),
            'is_subscription_addon': True if post.get(
                'subscription_addon') == 'on' else False,
            'list_price': float(post.get('sale_price')),
            'subscription_plan_id': int(post.get('subscription_plan')),
            'subscription_contract_id': int(post.get('subscription_contract')),
            'is_able_to_assign': True if post.get(
                'able_to_assign') == 'on' else False,
        }
        product.sudo().write(values)
        if post.get('photo'):
            product.sudo().write({
                'image_1920': base64.b64encode(post.get(
                    'photo').read())
            })
        return request.redirect(
            '/my/subscription_product_details/%s' % product.id)

    # Subscription Plan

    @http.route(['/my/update_subscription_plan'], type='http',
                auth='public', csrf=False, website=True,
                method='POST')
    def update_subscription_plan(self, **post):
        plan = request.env[
            'subscription.plan'].browse(int(post.get('plan_id')))
        task_ids = list(
            map(int, request.httprequest.form.getlist('stage_ids')))
        values = {
            'name': post.get('name'),
            'duration': int(post.get('duration')),
            'unit': post.get('duration_type'),
            'never_expires': True if post.get(
                'never_expires') == 'on' else False,
            'num_billing_cycle': int(post.get('num_billing_cycles')),
            'start_immediately': True if post.get(
                'start_immediate') == 'on' else False,
            'month_billing_day': int(post.get('month_billing_day')),
            'plan_amount': float(post.get('price')),
            'trial_period': True if post.get(
                'has_trial') == 'on' else False,
            'trial_duration': int(post.get('trial_duration')),
            'trial_duration_unit': post.get('trial_duration_unit'),
            'sessions': int(post.get('sessions')),
            'one2one': int(post.get('one2one')),
            'project_template_id': int(
                post.get('responsible_user')) if post.get(
                'project_template_id') else None,
            'override_product_price': True if post.get(
                'override_product_price') == 'on' else False,
        }
        plan.sudo().write(values)
        plan.sudo().write({
            'stage_ids': [(5, 0, 0)],
        })
        if task_ids:
            plan.sudo().write({
                'stage_ids': [(4, task) for task in task_ids]
            })
        return request.redirect('/my/subscription_plan_details/%s' % plan.id)

    @http.route(['/my/subscription_plan_details/<int:plan_id>'], type='http',
                auth='user', website=True)
    def subscription_plan_details(self, **kwargs):
        print("kw", kwargs)
        plan = request.env['subscription.plan'].sudo().browse(kwargs.get('plan_id'))
        print(plan)
        values = {
            'plan': plan,
            'is_account': True,
            'templates': request.env['project.project'].search([
                ('id', '!=', plan.project_template_id.id),
                ('active', '=', True),
                ('is_template', '=', True)
            ]),
            'stages': request.env['project.task.type'].search([
                ('id', 'not in', plan.stage_ids.ids)
            ])
        }
        return request.render(
            'sports_erp_dashboard.subscription_plan_details_template', values)

    @http.route(['/my/subscription_plans', '/my/subscription_plans/page/<int:page>'], type='http',
                auth='user', website=True)
    def subscription_plans_home(self, page=0, search='', **post):
        domain = [('company_id', '=', request.env.user.company_id.id), ]
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        subscription_plans = request.env['subscription.plan'].sudo().search(
            domain)
        print('subscription_plans', subscription_plans)
        total = len(subscription_plans)
        pager = request.website.pager(
            url='/my/subscription_plans',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        subscription_plans = subscription_plans[offset: offset + 6]
        values = {
            'search': search,
            'subscription_plans': subscription_plans,
            'pager': pager,
            'is_account': True,
            'total_subscription_plans': request.env[
                'subscription.plan'].sudo().search(
                [('company_id', '=', request.env.user.company_id.id)]),
            'total': total,
        }
        print(values)
        return request.render(
            'sports_erp_dashboard.subscription_plan_template', values)

    @http.route('/my/delete_subscription_plan/<int:subscription_plan>',
                type='http', auth='public', csrf=False, website=True)
    def delete_subscription(self, **kwargs):
        print("kw", kwargs)
        subscription_plan = request.env['subscription.plan'].sudo().browse(
            kwargs.get('subscription_plan')
        )
        subscription_plan.sudo().unlink()
        return request.redirect('/my/subscription_plans')

    @http.route('/create/subscription_plan', type='http',
                auth='public', csrf=False, website=True,
                method='POST')
    def create_subscription_plans(self, **post):
        task_ids = list(
            map(int, request.httprequest.form.getlist('task_stages')))
        values = {
            'name': post.get('plan_name'),
            'duration': int(post.get('duration')),
            'unit': post.get('duration_type'),
            'plan_amount': float(post.get('price')),
            'never_expires': True if post.get(
                'never_expires') == 'on' else False,
            'num_billing_cycle': int(post.get('billing_cycles')),
            'start_immediately': True if post.get(
                'start_immediate') == 'on' else False,
            'trial_period': True if post.get(
                'has_trial') == 'on' else False,
            'month_billing_day': int(post.get('billing_month_day')),
            'trial_duration': int(post.get('trial_duration')),
            'trial_duration_unit': post.get('trial_duration_type'),
            'sessions': int(post.get('no_of_sessions')),
            'one2one': int(post.get('one2one')),
            'stage_ids': [(4, task) for task in task_ids],
            'project_template_id': int(
                post.get('project_template_id')) if post.get(
                'project_template_id') else None,
            'override_product_price': True if post.get(
                'override_product_price') == 'on' else False,
            'company_id': request.env.user.company_id.id,
        }
        org_domain = []
        org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        if organisation:
            values['organisation_ids'] = [
                (4, organisation.id if organisation else False)]
        plan = request.env['subscription.plan'].sudo().create(values)
        return request.redirect('/my/subscription_plans')

    # Subscription Customers

    # @http.route('/my/delete_subscription_customer/<int:subscription_customer>',
    #             type='http', auth='public', csrf=False, website=True)
    # def subscription_customer(self, **kwargs):
    #     print('kw', kwargs)
    #     subscription_customer = request.env['res.partner'].sudo().browse(
    #         kwargs.get('subscription_customer')
    #     )
    #     print("sus", subscription_customer)
    #     subscription_customer.sudo().unlink()
    #     return request.redirect('/my/subscription_customers')
    #
    # @http.route(['/my/update_subscription_customer'], type='http',
    #             auth='public', csrf=False, website=True,
    #             methods=['POST', 'GET'])
    # def update_subscription_customer(self, **post):
    #     print('pos', post)
    #     customer = request.env['res.partner'].sudo().browse(
    #         int(post.get('subscription_customer_id')))
    #     values = {
    #         'name': post.get('name'),
    #         'last_name': post.get('last_name'),
    #         'email': post.get('email'),
    #         'city': post.get('city'),
    #         'zip': post.get('zip_code'),
    #         'phone': post.get('phone'),
    #         'street': post.get('street_name'),
    #         'state_id': int(post.get('state')),
    #         'country_id': int(post.get('country')),
    #     }
    #     customer.sudo().write(values)
    #     if post.get('photo'):
    #         customer.sudo().write({
    #             'image_1920': base64.b64encode(post.get(
    #                 'photo').read())
    #         })
    #     return request.redirect(
    #         '/my/subscription_customer_details/%s' % customer.id)
    #
    # @http.route(['/my/subscription_customer_details/<int:customer_id>'],
    #             type='http',
    #             auth='user', website=True)
    # def subscription_customer_details(self, **kwargs):
    #     print("kwa", kwargs)
    #     subscription_customer = request.env['res.partner'].sudo().browse(
    #         kwargs.get('customer_id')
    #     )
    #     values = {
    #         'subscription_customer': subscription_customer,
    #         'is_account': True,
    #         'countries': request.env[
    #             'res.country'].sudo().search([
    #             ('id', '!=', subscription_customer.country_id.id)
    #         ]),
    #         'states': request.env[
    #             'res.country.state'].sudo().search([
    #             ('id', '!=', subscription_customer.state_id.id)
    #         ])
    #
    #     }
    #     return request.render(
    #         'sports_erp_dashboard.subscription_customer_details_template',
    #         values)
    #
    # @http.route(['/my/subscription_customers',
    #              '/my/subscription_customers/page/<int:page>'],
    #             type='http',
    #             auth='user', website=True)
    # def subscription_customers_home(self, page=0, search='', **post):
    #     domain = []
    #     org_domain = []
    #     org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
    #     if request.httprequest.cookies.get('select_organisation') != 0:
    #         org_domain.append(('id', '=',
    #                            request.httprequest.cookies.get(
    #                                'select_organisation')))
    #     organisation = request.env['organisation.organisation'].sudo().search(
    #         org_domain, limit=1)
    #     if search:
    #         domain.append(('name', 'ilike', search))
    #         post["search"] = search
    #     if organisation:
    #         domain.append(('organisation_ids', 'in', [organisation.id]))
    #     domain.append(
    #         ('company_id', 'in', [request.env.user.company_id.id, False]))
    #     subscription_customers = request.env['res.partner'].sudo().search(
    #         domain)
    #     total = len(subscription_customers)
    #     pager = request.website.pager(
    #         url='/my/subscription_customers',
    #         total=total,
    #         page=page,
    #         step=6,
    #     )
    #     offset = pager['offset']
    #     subscription_customers = subscription_customers[offset: offset + 6]
    #     print("sus", subscription_customers)
    #     values = {
    #         'search': search,
    #         'subscription_customers': subscription_customers,
    #         'pager': pager,
    #         'is_account': True,
    #         'total_subscription_customers': request.env[
    #             'res.partner'].sudo().search(
    #             [])
    #     }
    #     print("values", values)
    #     return request.render(
    #         'sports_erp_dashboard.subscription_customer_template', values)
    #
    # @http.route('/create/subscription_customer', type='http',
    #             auth='public', csrf=False, website=True,
    #             method='POST')
    # def create_customer(self, **post):
    #     print("pos", post)
    #     org_domain = []
    #     org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
    #     if request.httprequest.cookies.get('select_organisation') != 0:
    #         org_domain.append(('id', '=',
    #                            request.httprequest.cookies.get(
    #                                'select_organisation')))
    #     organisation = request.env['organisation.organisation'].sudo().search(
    #         org_domain, limit=1)
    #     values = {
    #         'name': post.get('customer_name'),
    #         'last_name': post.get('last_name'),
    #         'phone': post.get('phone'),
    #         'email': post.get('email'),
    #         'street': post.get('street_name'),
    #         'city': post.get('city_name'),
    #         'state_id': int(post.get('state_id')),
    #         'zip': post.get('zip_code'),
    #         'country_id': int(post.get('country_id')),
    #         'company_id': request.env.user.company_id.id
    #     }
    #     if organisation:
    #         values['organisation_ids'] = [
    #             (4, organisation.id if organisation else False)]
    #     customer = request.env['res.partner'].sudo().create(values)
    #     if post.get('photo'):
    #         customer.sudo().write({
    #             'image_1920': base64.b64encode(post.get(
    #                 'photo').read())
    #         })
#     return request.redirect('/my/subscription_customers')