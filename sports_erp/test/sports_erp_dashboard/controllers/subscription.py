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
    @http.route(['/subscriptions', '/subscriptions/page/<int:page>', '/subscriptions', '/subscriptions/page/<int:page>'], type='http', auth="user", website=True)
    def subscriptions(self, page=1, search=''):
        Subscription = request.env['product.template'].sudo().search([])
        org_domain = []
        if request.env.user.has_group('organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        else:
            org_domain.append(('id', 'in', request.env.user.partner_id.organisation_ids.ids))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        domain = [('activate_subscription', '=', True), ('is_able_to_assign', '=', True), ('is_published', '=', True), ('organisation_ids', '=', organisation.id)]

        if search:
            domain.append(('name', 'ilike', search))
        subscriptions = Subscription.sudo().search(domain)
        return request.render('sports_erp_dashboard.subscription_home_template',
                              {'subscription': subscriptions,
                               'is_account': True
                              })

    # Subscription
    @http.route(['/my/subscriptions', '/my/subscriptions/page/<int:page>'], type='http',
                auth='user', website=True)
    def subscription_home(self, page=0, search='', **post):
        print('pos', post)
        domain = []
        org_domain = []
        filtered_contracts = list(
            map(int, request.httprequest.form.getlist('filtered_contracts')))
        filtered_products = list(
            map(int, request.httprequest.form.getlist('filtered_products')))
        filtered_plans = list(
            map(int, request.httprequest.form.getlist('filtered_plans')))


        # else:
        #     org_domain.append(
        #         ('id', 'in', request.env.user.partner_id.organisation_ids.ids))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))

        if request.env.user.has_group(
                'organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        elif request.env.user.has_group(
                'organisation.group_organisation_coaches'):
            coaches = request.env['organisation.coaches'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)])
            org_domain.append(('id', 'in', coaches.organisation_ids.ids))
        elif request.env.user.has_group(
                'organisation.group_organisation_parents'):
            parents = request.env['organisation.parents'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])
            partners = parents.athlete_ids.mapped('partner_id').ids
            print(partners, "parents")
            domain.append(('customer_name', 'in', partners))
        else:
            domain.append(('customer_name', '=', request.env.user.partner_id.id))
            # organisation = request.env[
            #     'organisation.organisation'].sudo().search(org_domain, limit=1)
        print(org_domain, "domain")
        organisation = []
        if org_domain:
            organisation = request.env[
                'organisation.organisation'].sudo().search(
                org_domain, limit=1).ids
        if organisation:
            domain.append(('organisation_ids', 'in', organisation))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        if filtered_contracts:
            domain.append(('contract_id', 'in', filtered_contracts))
        if filtered_products:
            domain.append(('product_id', 'in', filtered_products))
        if filtered_plans:
            domain.append(('sub_plan_id', 'in', filtered_plans))
        domain.append(('company_id', '=', request.env.user.company_id.id))
        print(domain, "domain")
        subscription = request.env['subscription.subscription'].sudo().search(
            domain)
        customers = request.env['res.partner'].sudo().search(
            [('id', '!=', request.env.user.partner_id.id),
             ('organisation_ids', 'in', organisation),
             ('company_id', '=', request.env.user.company_id.id)])
        contracts = request.env['subscription.contract'].sudo().search([
            ('organisation_ids', 'in', organisation),
            ('company_id', '=', request.env.user.company_id.id)])
        products = request.env['product.product'].sudo().search([
            ('organisation_ids', 'in', organisation),
            ('company_id', '=', request.env.user.company_id.id)])
        plans = request.env['subscription.plan'].sudo().search([
            ('organisation_ids', 'in', organisation),
            ('company_id', '=', request.env.user.company_id.id)])
        print(subscription)
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
            'total_subscriptions': subscription,
            'customers': customers,
            'contracts': contracts,
            'products': products,
            'plans': plans,
            'total': total,
            'filtered_contracts': request.env[
                'subscription.contract'].sudo().browse(filtered_contracts),
            'filtered_products': request.env[
                'product.product'].sudo().browse(filtered_products),
            'filtered_plans': request.env[
                'subscription.plan'].sudo().browse(filtered_plans),
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
                auth='user', csrf=False, website=True,
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
                auth='user', csrf=False, website=True,
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
                auth='user', csrf=False, website=True,
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
        if organisation:
            domain.append(('organisation_ids', '=', [organisation.id]))
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
                type='http', auth='user', csrf=False, website=True)
    def delete_subscription_product(self, **kwargs):
        subscription_product = request.env['product.product'].sudo().browse(
            kwargs.get('subscription_product'))
        subscription_product.sudo().unlink()
        return request.redirect('/my/subscription_products')

    @http.route(['/create/subscription_product'], type='http',
                auth='user', csrf=False, website=True,
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
                type='http', auth='user', csrf=False, website=True)
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
                auth='user', csrf=False, website=True,
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
                auth='user', csrf=False, website=True,
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
        org_domain = []
        if request.env.user.has_group('organisation.group_organisation_administrator'):
            org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        else:
            org_domain.append(('id', 'in', request.env.user.partner_id.organisation_ids.ids))
        if request.httprequest.cookies.get('select_organisation') is not None:
            org_domain.append(('id', '=',
                               request.httprequest.cookies.get(
                                   'select_organisation')))
        organisation = request.env['organisation.organisation'].sudo().search(
            org_domain, limit=1)
        if organisation:
            domain.append(('organisation_ids', '=', [organisation.id] ))
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
                type='http', auth='user', csrf=False, website=True)
    def delete_subscription(self, **kwargs):
        print("kw", kwargs)
        subscription_plan = request.env['subscription.plan'].sudo().browse(
            kwargs.get('subscription_plan')
        )
        subscription_plan.sudo().unlink()
        return request.redirect('/my/subscription_plans')

    @http.route('/create/subscription_plan', type='http',
                auth='user', csrf=False, website=True,
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
