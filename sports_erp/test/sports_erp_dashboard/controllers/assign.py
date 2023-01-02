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


class Assign(CustomerPortal):
    @http.route(['/assign/coach'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def assign_coach(self, **post):
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
        customer_ids = list(
            map(int,
                request.httprequest.form.getlist('assigned')))
        if post.get('subscription') and customer_ids:
            product = request.env['product.product'].sudo().search(
                [('id', '=', int(post.get('subscription')))])
            tax_ids = list(
                map(int,
                    request.httprequest.form.getlist('subscription_taxes')))
            for rec in customer_ids:
                values = {
                    'active': True,
                    'contract_id': product.subscription_contract_id.id,
                    'customer_name': rec,
                    'customer_billing_address': rec,
                    'company_id': request.env.user.company_id.id,
                    'product_id': int(post.get('subscription')),
                    'tax_id': [(4, tax) for tax in tax_ids],
                    'quantity': float(post.get('quantity')),
                    'sub_plan_id': product.subscription_plan_id.id,
                    'price': product.subscription_plan_id.plan_amount if product.subscription_plan_id.override_product_price else product.lst_price,
                    'duration': product.subscription_plan_id.duration,
                    'unit': product.subscription_plan_id.unit,
                    'start_date': post.get('start_date') if post.get(
                        'start_date') else False,
                    'end_date': post.get('end_date') if post.get(
                        'end_date') else False,
                }
                if organisation:
                    values['organisation_ids'] = [
                        (4, organisation.id if organisation else False)]
                subscription = request.env[
                    'subscription.subscription'].sudo().create(
                    values)
                subscription.get_confirm_subscription()
        partners = list(
            map(int, request.httprequest.form.getlist('user_ids')))
        if post.get('booking_type') and partners:
            user_ids = request.env['res.users'].sudo().search([
                ('partner_id', 'in', partners)
            ]).ids
            values = {
                'appointment_type_id': int(
                    post.get('booking_type')) if post.get(
                    'booking_type') else None,
                'date': post.get('date'),
                'user_ids': [(4, user) for user in user_ids]}
            request.env['booking.booking'].sudo().create(values)
        member_ids = list(
            map(int, request.httprequest.form.getlist('members')))
        if post.get('channels') and member_ids:
            chathub = request.env[
                'chat.hub'].sudo().browse(int(post.get('channels')))
            chathub.sudo().write({
                'partner_ids': [(4, member) for member in member_ids]
            })
        return request.redirect('/my/coaches')

    @http.route(['/assign/athlete'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def assign_athlete(self, **post):
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
        customer_ids = list(
            map(int,
                request.httprequest.form.getlist('assigned')))
        if post.get('subscription') and customer_ids:
            product = request.env['product.product'].sudo().search(
                [('id', '=', int(post.get('subscription')))])
            tax_ids = list(
                map(int,
                    request.httprequest.form.getlist('subscription_taxes')))
            for rec in customer_ids:
                values = {
                    'active': True,
                    'contract_id': product.subscription_contract_id.id,
                    'customer_name': rec,
                    'customer_billing_address': rec,
                    'company_id': request.env.user.company_id.id,
                    'product_id': int(post.get('subscription')),
                    'tax_id': [(4, tax) for tax in tax_ids],
                    'quantity': float(post.get('quantity')),
                    'sub_plan_id': product.subscription_plan_id.id,
                    'price': product.subscription_plan_id.plan_amount if product.subscription_plan_id.override_product_price else product.lst_price,
                    'duration': product.subscription_plan_id.duration,
                    'unit': product.subscription_plan_id.unit,
                    'start_date': post.get('start_date') if post.get(
                        'start_date') else False,
                    'end_date': post.get('end_date') if post.get(
                        'end_date') else False,
                }
                if organisation:
                    values['organisation_ids'] = [
                        (4, organisation.id if organisation else False)]
                subscription = request.env[
                    'subscription.subscription'].sudo().create(
                    values)
                subscription.get_confirm_subscription()
        partners = list(
            map(int, request.httprequest.form.getlist('user_ids')))
        if post.get('booking_type') and partners:
            user_ids = request.env['res.users'].sudo().search([
                ('partner_id', 'in', partners)
            ]).ids
            values = {
                'appointment_type_id': int(
                    post.get('booking_type')) if post.get(
                    'booking_type') else None,
                'date': post.get('date'),
                'user_ids': [(4, user) for user in user_ids]}
            request.env['booking.booking'].sudo().create(values)
        member_ids = list(
            map(int, request.httprequest.form.getlist('members')))
        if post.get('channels') and member_ids:
            chathub = request.env[
                'chat.hub'].sudo().browse(int(post.get('channels')))
            chathub.sudo().write({
                'partner_ids': [(4, member) for member in member_ids]
            })
        return request.redirect('/my/athletes/home')

    @http.route(['/assign/parent'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def assign_parent(self, **post):
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
        customer_ids = list(
            map(int,
                request.httprequest.form.getlist('assigned')))
        print(customer_ids, 'custom')
        if post.get('subscription') and customer_ids:
            product = request.env['product.product'].sudo().search(
                [('id', '=', int(post.get('subscription')))])
            tax_ids = list(
                map(int,
                    request.httprequest.form.getlist('subscription_taxes')))
            for rec in customer_ids:
                values = {
                    'active': True,
                    'contract_id': product.subscription_contract_id.id,
                    'customer_name': rec,
                    'customer_billing_address': rec,
                    'company_id': request.env.user.company_id.id,
                    'product_id': int(post.get('subscription')),
                    'tax_id': [(4, tax) for tax in tax_ids],
                    'quantity': float(post.get('quantity')),
                    'sub_plan_id': product.subscription_plan_id.id,
                    'price': product.subscription_plan_id.plan_amount if product.subscription_plan_id.override_product_price else product.lst_price,
                    'duration': product.subscription_plan_id.duration,
                    'unit': product.subscription_plan_id.unit,
                    'start_date': post.get('start_date') if post.get(
                        'start_date') else False,
                    'end_date': post.get('end_date') if post.get(
                        'end_date') else False,
                }
                if organisation:
                    values['organisation_ids'] = [
                        (4, organisation.id if organisation else False)]
                subscription = request.env[
                    'subscription.subscription'].sudo().create(
                    values)
                subscription.get_confirm_subscription()
        partners = list(
            map(int, request.httprequest.form.getlist('user_ids')))
        if post.get('booking_type') and partners:
            user_ids = request.env['res.users'].sudo().search([
                ('partner_id', 'in', partners)
            ]).ids
            values = {
                'appointment_type_id': int(
                    post.get('booking_type')) if post.get(
                    'booking_type') else None,
                'date': post.get('date'),
                'user_ids': [(4, user) for user in user_ids]}
            request.env['booking.booking'].sudo().create(values)
        member_ids = list(
            map(int, request.httprequest.form.getlist('members')))
        if post.get('channels') and member_ids:
            chathub = request.env[
                'chat.hub'].sudo().browse(int(post.get('channels')))
            chathub.sudo().write({
                'partner_ids': [(4, member) for member in member_ids]
            })
        return request.redirect('/my/parents')

    @http.route(['/assign/group'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def assign_group(self, **post):
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
        group_ids = list(
            map(int,
                request.httprequest.form.getlist('assigned')))
        print(group_ids, 'group_ids')
        groups = request.env[
            'athlete.groups'].sudo().browse(group_ids)
        print(groups, 'groups')
        athlete_ids = groups.mapped(lambda x: x.athlete_ids.id)
        customer_ids = request.env[
            'organisation.athletes'].sudo().browse(
            athlete_ids).mapped(lambda x: x.partner_id.id)
        if post.get('subscription') and customer_ids:
            product = request.env['product.product'].sudo().search(
                [('id', '=', int(post.get('subscription')))])
            tax_ids = list(
                map(int,
                    request.httprequest.form.getlist('subscription_taxes')))
            print(customer_ids, 'custom')
            for rec in customer_ids:
                if rec:
                    values = {
                        'active': True,
                        'contract_id': product.subscription_contract_id.id,
                        'customer_name': rec,
                        'customer_billing_address': rec,
                        'company_id': request.env.user.company_id.id,
                        'product_id': int(post.get('subscription')),
                        'tax_id': [(4, tax) for tax in tax_ids],
                        'quantity': float(post.get('quantity')),
                        'sub_plan_id': product.subscription_plan_id.id,
                        'price': product.subscription_plan_id.plan_amount if product.subscription_plan_id.override_product_price else product.lst_price,
                        'duration': product.subscription_plan_id.duration,
                        'unit': product.subscription_plan_id.unit,
                        'start_date': post.get('start_date') if post.get(
                            'start_date') else False,
                        'end_date': post.get('end_date') if post.get(
                            'end_date') else False,
                    }
                    if organisation:
                        values['organisation_ids'] = [
                            (4, organisation.id if organisation else False)]
                    subscription = request.env[
                        'subscription.subscription'].sudo().create(
                        values)
                    subscription.get_confirm_subscription()

        group_booking = list(
            map(int,
                request.httprequest.form.getlist('user_ids')))
        booking_groups = request.env[
            'athlete.groups'].sudo().browse(group_booking)
        athlete_booking_ids = booking_groups.mapped(lambda x: x.athlete_ids.id)
        customer_booking = request.env[
            'organisation.athletes'].sudo().browse(
            athlete_booking_ids).mapped(lambda x: x.partner_id.id)
        if post.get('booking_type') and customer_booking:
            user_ids = request.env['res.users'].sudo().search([
                ('partner_id', 'in', customer_booking)
            ]).ids
            values = {
                'appointment_type_id': int(
                    post.get('booking_type')) if post.get(
                    'booking_type') else None,
                'date': post.get('date'),
                'user_ids': [(4, user) for user in user_ids]}
            request.env['booking.booking'].sudo().create(values)

        group_chat = list(
            map(int,
                request.httprequest.form.getlist('user_ids')))
        chat_groups = request.env[
            'athlete.groups'].sudo().browse(group_booking)
        athlete_chat_ids = chat_groups.mapped(lambda x: x.athlete_ids.id)
        customer_chat = request.env[
            'organisation.athletes'].sudo().browse(
            athlete_chat_ids).mapped(lambda x: x.partner_id.id)
        if post.get('channels') and customer_chat:
            chathub = request.env[
                'chat.hub'].sudo().browse(int(post.get('channels')))
            chathub.sudo().write({
                'partner_ids': [(4, member) for member in customer_chat]
            })
        return request.redirect('/my/athletes/home')

    @http.route(['/assign/fan'], type='http',
                auth='user', csrf=False, website=True,
                methods=['POST', 'GET'])
    def assign_fan(self, **post):
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
        customer_ids = list(
            map(int,
                request.httprequest.form.getlist('assigned')))
        print(customer_ids, 'custom')
        if post.get('subscription') and customer_ids:
            product = request.env['product.product'].sudo().search(
                [('id', '=', int(post.get('subscription')))])
            tax_ids = list(
                map(int,
                    request.httprequest.form.getlist('subscription_taxes')))
            for rec in customer_ids:
                values = {
                    'active': True,
                    'contract_id': product.subscription_contract_id.id,
                    'customer_name': rec,
                    'customer_billing_address': rec,
                    'company_id': request.env.user.company_id.id,
                    'product_id': int(post.get('subscription')),
                    'tax_id': [(4, tax) for tax in tax_ids],
                    'quantity': float(post.get('quantity')),
                    'sub_plan_id': product.subscription_plan_id.id,
                    'price': product.subscription_plan_id.plan_amount if product.subscription_plan_id.override_product_price else product.lst_price,
                    'duration': product.subscription_plan_id.duration,
                    'unit': product.subscription_plan_id.unit,
                    'start_date': post.get('start_date') if post.get(
                        'start_date') else False,
                    'end_date': post.get('end_date') if post.get(
                        'end_date') else False,
                }
                if organisation:
                    values['organisation_ids'] = [
                        (4, organisation.id if organisation else False)]
                subscription = request.env[
                    'subscription.subscription'].sudo().create(
                    values)
                subscription.get_confirm_subscription()
        partners = list(
            map(int, request.httprequest.form.getlist('user_ids')))
        if post.get('booking_type') and partners:
            user_ids = request.env['res.users'].sudo().search([
                ('partner_id', 'in', partners)
            ]).ids
            values = {
                'appointment_type_id': int(
                    post.get('booking_type')) if post.get(
                    'booking_type') else None,
                'date': post.get('date'),
                'user_ids': [(4, user) for user in user_ids]}
            request.env['booking.booking'].sudo().create(values)
        member_ids = list(
            map(int, request.httprequest.form.getlist('members')))
        if post.get('channels') and member_ids:
            chathub = request.env[
                'chat.hub'].sudo().browse(int(post.get('channels')))
            chathub.sudo().write({
                'partner_ids': [(4, member) for member in member_ids]
            })
        return request.redirect('/my/fans')
