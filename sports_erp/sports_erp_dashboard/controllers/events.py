import base64
import json
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.http_routing.models.ir_http import slug
from odoo import fields, _
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager
from collections import OrderedDict
from odoo.http import request, route
from odoo.addons.base.models.res_partner import _tz_get
import pytz


class EventsPortal(CustomerPortal):

    # Events
    @route(['/my/events', '/my/events/page/<int:page>'],
           type='http', auth="user", website=True)
    def my_events(self, search='', page=0, **post):
        _tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda
            tz: tz if not tz.startswith('Etc/') else '_')]
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
        domain.append(('company_id', '=', request.env.user.company_id.id))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        events = request.env['event.event'].sudo().search(domain)
        # athletes = request.env['organisation.athletes'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        # parents = request.env['organisation.parents'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        # # coaches = request.env['organisation.coaches'].sudo().search(
        # #     [('organisation_ids', 'in', [organisation.id])])
        # groups = request.env['athlete.groups'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        # disciplines = request.env['organisation.discipline'].sudo().search(
        #     [('organisation_ids', 'in', [organisation.id])])
        total = len(events)
        pager = request.website.pager(
            url='/my/events',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        events = events[offset: offset + 5]
        values = {
            'search': search,
            'events': events,
            'time_zone': _tzs,
            # 'athletes': athletes,
            # 'parents': parents,
            # 'groups': groups,
            # 'disciplines': disciplines,
            'pager': pager,
            'is_account': True,
            'total': total,
            # 'organisations': request.env[
            #     'organisation.organisation'].sudo().search(
            #     [('allowed_user_ids', 'in', [request.env.user.id])]),
            # 'total_coaches': coaches
        }
        return request.render('sports_erp_dashboard.event_template', values)

    @http.route('/create/event', type='http', auth='user',
                website=True)
    def create_website_event(self, **post):
        print(post, "post.......")
        start_date = post.get('datetimes').split(' - ')
        print(start_date)
        tag_ids = list(
            map(int, request.httprequest.form.getlist('tags')))
        event = request.env['event.event'].sudo().create({
            'name': post.get('name'),
            'is_published': True if post.get('is_published') == 'on' else False,
            'date_begin': start_date[0],
            'date_end': start_date[1],
            'event_type_id': int(post.get('template')) if post.get('template') else None,
            'seats_limited': True if post.get('limit_reg') == 'on' else False,
            'auto_confirm': True if post.get('auto_confirmation') == 'on' else False,
            'menu_register_cta': True if post.get('register_button') == 'on' else False,
            'seats_max': post.get('no_attendees') if post.get('limit_reg') == 'on' else False,
            'address_id': int(post.get('venue')) if post.get('venue') else None,
            'organizer_id': int(post.get('organizer')) if post.get('organizer') else None,
            'user_id': int(post.get('responsible')) if post.get('responsible') else None,
            'tag_ids': [(4, tag) for tag in tag_ids],
        })
        print(event.read())
        return request.redirect('/my/events')

    @route(['/my/event/detail'],
           type='http', auth="user", website=True)
    def my_events_details(self, **kw):
        print(kw)
        event = request.env['event.event'].sudo().browse(
            int(kw.get('event')))
        # _tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda
        #     tz: tz if not tz.startswith('Etc/') else '_')]
        return request.render('sports_erp_dashboard.event_details', {
            'event': event,
            'is_account': True
        })

    @http.route('/my/event/delete', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def delete_event(self, **post):
        print(post)
        if post.get('event'):
            event = request.env['event.event'].sudo().browse(
                int(post.get('event')))
            event.sudo().unlink()
        return request.redirect('/my/events')

    @http.route('/update/event', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def update_event(self, **post):
        if post.get('event'):
            start_date = post.get('datetimes').split(' - ')
            print(start_date)
            tag_ids = list(
                map(int, request.httprequest.form.getlist('tags')))
            event = request.env['event.event'].sudo().browse(
                int(post.get('event')))
            event.sudo().write({
                 'name': post.get('name'),
            'is_published': True if post.get('is_published') == 'on' else False,
            'date_begin': start_date[0],
            'date_end': start_date[1],
            'event_type_id': int(post.get('template')) if post.get('template') else None,
            'seats_limited': True if post.get('limit_reg') == 'on' else False,
            'auto_confirm': True if post.get('auto_confirmation') == 'on' else False,
            'menu_register_cta': True if post.get('register_button') == 'on' else False,
            'event_extension': True if post.get('event_extension') == 'on' else False,
            'seats_max': post.get('no_attendees'),
            'website_menu': True if post.get('website_menu') == 'on' else False,
            'address_id': int(post.get('venue')) if post.get('venue') else None,
            'organizer_id': int(post.get('organizer')) if post.get('organizer') else None,
            'user_id': int(post.get('responsible')) if post.get('responsible') else None,
            'tag_ids': [(4, tag) for tag in tag_ids],
            })
            return request.redirect(
                '/my/event/detail?event=%s' % event.id)


    # Event Templates
    @route(['/my/event/templates', '/my/event/templates/page/<int:page>'],
           type='http', auth="user", website=True)
    def my_events_templates(self, search='', page=0, **post):
        domain = []
        print(_tz_get, "tz_get")
        _tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda
            tz: tz if not tz.startswith('Etc/') else '_')]
        print(_tzs)
        # org_domain = []
        # org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        # if request.httprequest.cookies.get('select_organisation') is not None:
        #     org_domain.append(('id', '=',
        #                        request.httprequest.cookies.get(
        #                            'select_organisation')))
        # organisation = request.env['organisation.organisation'].sudo().search(
        #     org_domain, limit=1)
        # if organisation:
        #     domain.append(('organisation_ids', 'in', [organisation.id]))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        event_types = request.env['event.type'].sudo().search(domain)
        total = len(event_types)
        pager = request.website.pager(
            url='/my/event/templates',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        event_types = event_types[offset: offset + 6]
        values = {
            'search': search,
            'event_types': event_types,
            'time_zone': _tzs,
            'tags': request.env['event.tag'].sudo().search([]),
            'pager': pager,
            'is_account': True,
            'total': total,
            # 'organisations': request.env[
            #     'organisation.organisation'].sudo().search(
            #     [('allowed_user_ids', 'in', [request.env.user.id])]),
            # 'total_coaches': coaches
        }
        return request.render('sports_erp_dashboard.event_template_page', values)

    @http.route('/create/event/template', type='http', auth='user', website=True)
    def create_event_template(self, **post):
        event_template = request.env['event.type'].sudo().create({
            'name': post.get('event_template'),
            'default_timezone': post.get('time_zone'),
            'website_menu': True if post.get('website_menu') == 'on' else False,
            'menu_register_cta': True if post.get('register_button') == 'on' else False,
            'has_seats_limitation': True if post.get('limit_reg') == 'on' else False,
            'auto_confirm': True if post.get('auto_confirm') == 'on' else False,
            'note': post.get('notes'),
            'ticket_instructions': post.get('extra_info'),
        })
        return request.redirect('/my/event/templates')

    @route(['/my/event/template/detail'],
           type='http', auth="user", website=True)
    def my_events_template_details(self, **kw):
        print(kw)
        event_type = request.env['event.type'].sudo().browse(
            int(kw.get('type_id')))
        _tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda
            tz: tz if not tz.startswith('Etc/') else '_')]
        return request.render('sports_erp_dashboard.event_template_details', {
            'event_type': event_type,
            'time_zone': _tzs,
            'is_account': True
        })

    @http.route('/my/event/template/delete', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def delete_event_template(self, **post):
        if post.get('event_id'):
            event_type = request.env['event.type'].sudo().browse(int(post.get('event_id')))
            event_type.sudo().unlink()
        return request.redirect('/my/event/templates')

    @http.route('/update/event/template', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def update_event_template(self, **post):
        if post.get('event_type'):
            event_type = request.env['event.type'].sudo().browse(
                int(post.get('event_type')))
            event_type.sudo().write({
                'name': post.get('name'),
                'default_timezone': post.get('time_zone'),
                'website_menu': True if post.get('website_menu') == 'on' else False,
                'menu_register_cta': True if post.get('register_button') == 'on' else False,
                'has_seats_limitation': True if post.get('limit_reg') == 'on' else False,
                'auto_confirm': True if post.get('auto_confirm') == 'on' else False,
                'note': post.get('notes'),
                'ticket_instructions': post.get('extra_info'),
            })
            return request.redirect(
                '/my/event/template/detail?type_id=%s' % event_type.id)

    @http.route('/update/event_template', auth='user', type='json', website=True)
    def event_template_update(self, **post):
        print(post, "dfghjkl")
        event_template = request.env['event.type'].sudo().browse(int(post.get('template')))
        if event_template:
            event_template.sudo().write({
                'name': post.get('name'),
                'default_timezone': post.get('timezone'),
                'website_menu': post.get(
                    'website_menu'),
                'menu_register_cta': post.get(
                    'register_button'),
                'has_seats_limitation': post.get(
                    'limit_reg'),
                'auto_confirm': post.get(
                    'auto_confirm'),
                'note': post.get('notes'),
                'ticket_instructions': post.get('extra_info'),
            })
        event_template.sudo().write({
            'event_type_ticket_ids': [(5, 0, 0)]
        })
        if post.get('ticket_lines'):
            for line in post.get('ticket_lines'):

                event_template.sudo().write({
                    'event_type_ticket_ids': [(0, 0, {
                        'name': line['name'],
                        'product_id': int(line['product_id']),
                        'description': line['description'],
                        'seats_max': line['max'],
                        'price': line['price']
                        # 'start_date'
                    })]
                })
                print(line, "line")
        return True
    # Event Stages
    @route(['/my/event/stages', '/my/event/stage', '/my/event/stages/page/<int:page>'],
           type='http', auth="user", website=True)
    def my_events_stages(self, search='', page=0, **post):
        domain = []

        # org_domain = []
        # org_domain.append(('allowed_user_ids', 'in', [request.env.user.id]))
        # if request.httprequest.cookies.get('select_organisation') is not None:
        #     org_domain.append(('id', '=',
        #                        request.httprequest.cookies.get(
        #                            'select_organisation')))
        # organisation = request.env['organisation.organisation'].sudo().search(
        #     org_domain, limit=1)
        # if organisation:
        #     domain.append(('organisation_ids', 'in', [organisation.id]))
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        event_stage = request.env['event.stage'].sudo().search(domain)
        total = len(event_stage)
        pager = request.website.pager(
            url='/my/event/stage',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        event_stage = event_stage[offset: offset + 6]
        values = {
            'search': search,
            'event_stage': event_stage,
            'pager': pager,
            'is_account': True,
            'total': total,
            # 'organisations': request.env[
            #     'organisation.organisation'].sudo().search(
            #     [('allowed_user_ids', 'in', [request.env.user.id])]),
            # 'total_coaches': coaches
        }
        print(values)
        return request.render('sports_erp_dashboard.event_stages_page', values)

    @route(['/my/event/stage/detail'],
           type='http', auth="user", website=True)
    def my_events_stage_details(self, **kw):
        print("Tyyyyyy")
        stage = request.env['event.stage'].sudo().browse(
            int(kw.get('stage')))
        return request.render('sports_erp_dashboard.event_stage_details', {
            'event_stage': stage,
            'is_account': True
        })

    @http.route('/create/event/stage', type='http', auth='user',
                website=True)
    def create_event_stage(self, **post):
        event_stage = request.env['event.stage'].sudo().create({
            'name': post.get('name'),
            'fold': True if post.get('folded') == 'on' else False,
            'pipe_end': True if post.get('end_stage') == 'on' else False,
            'description': post.get('description'),
            'sequence': post.get('sequence'),
        })
        return request.redirect('/my/event/stages')

    @http.route('/my/event/stage/delete', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def delete_event_stage(self, **post):
        if post.get('stage'):
            event_stage = request.env['event.stage'].sudo().browse(
                int(post.get('stage')))
            event_stage.sudo().unlink()
        return request.redirect('/my/event/stages')

    @http.route('/update/event/stage', type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def update_event_stage(self, **post):
        if post.get('stage'):
            stage = request.env['event.stage'].sudo().browse(
                int(post.get('stage')))
            event_stage = stage.sudo().write({
                'name': post.get('name'),
                'fold': True if post.get('folded') == 'on' else False,
                'pipe_end': True if post.get('end_stage') == 'on' else False,
                'description': post.get('description'),
                'sequence': post.get('sequence'),
            })
            return request.redirect('/my/event/stage/detail?stage=%s' % stage.id)

    # Event Tag Categories
    @route(['/create/event/tag/categories'],
           type='http', auth="user", website=True)
    def create_events_tags_categories(self, **kw):
        print(kw, "kw")
        categories = request.env['event.tag.category'].sudo().create({
            'name': kw.get('name'),
            'is_published': True
        })
        list = kw.get('tags').split(',')
        print(list)
        for tag in list:
            event_tag = request.env['event.tag'].sudo().create({
                'name': tag,
                'category_id': categories.id
            })

        return request.redirect('/my/events')

    @http.route('/get_products', auth='user', type='json', website=True)
    def get_products(self, **kwargs):
        products = request.env['product.product'].sudo().search(
            [('detailed_type', '=', 'event')])
        product_ids = []
        for product in products:
            product_ids.append([product.display_name, product.id])
        return {
            'product_ids': product_ids,
        }

    @http.route(['/my/event/tag_category', '/my/event/tag_category/page/<int:page>'],
                type='http', auth="user", website=True)
    def event_tag_category(self, search='', page=0, **post):
        domain = []
        if search:
            domain.append(('name', 'ilike', search))
            post["search"] = search
        tag_category = request.env['event.tag.category'].sudo().search(domain)
        total = len(tag_category)
        pager = request.website.pager(
            url='/my/event/tag_category',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        tag_category = tag_category[offset: offset + 5]
        values = {
            'search': search,
            'tags': tag_category,
            'is_account': True,
            'total': total,
            'pager': pager,
        }
        return request.render(
            'sports_erp_dashboard.event_tag_category_template', values)

    @http.route(
        ['/my/event/tag_category/tag_id=<int:tag_id>'],
        type='http', auth="user", website=True)
    def event_tag_category_details(self, **kw):
        tag_category = request.env['event.tag.category'].sudo().browse(
            kw.get('tag_id'))

        values = {
            'is_account': True,
            'tag_category': tag_category,
            'tags': request.env['event.tag'].sudo().search(
                [('id', 'not in', tag_category.tag_ids.ids)]),
        }
        return request.render(
            'sports_erp_dashboard.event_tag_category_details', values)

    @http.route(['/update/event_tag_category_details'],
                type='http',
                auth='user', csrf=False, website=True,
                method='POST')
    def update_event_category_details(self, **post):
        print('post', post)
        tag_ids = list(
            map(int, request.httprequest.form.getlist('tag_ids')))
        print(tag_ids)
        tag_category = request.env['event.tag.category'].sudo().browse(
            int(post.get('tag_category')))
        tag_category.sudo().write({
            'name': post.get('name'),
            'is_published': True if post.get(
                'show_on_website') == 'on' else False,
        })
        tag_category.sudo().write({
            'tag_ids': [(5, 0, 0)]
        })
        if tag_ids:
            tag_category.sudo().write({
                'tag_ids': [(4, tag) for tag in tag_ids]})

        return request.redirect(
            '/my/event/tag_category/tag_id=%s' % tag_category.id)

    @http.route(['/remove_tag_category/tag_id=<int:tag_id>'],
                type='http', auth="user", website=True)
    def remove_tag_category(self, **kw):
        print('post', kw)
        tag_category = request.env['event.tag.category'].sudo().browse(
            kw.get('tag_id'))
        tag_category.sudo().unlink()
        return request.redirect('/my/event/tag_category')


class WebsiteEventControllerExtended(WebsiteEventController):

    def sitemap_event(env, rule, qs):
        if not qs or qs.lower() in '/events':
            yield {'loc': '/events'}

    @http.route(['/event', '/event/page/<int:page>', '/events',
                 '/events/page/<int:page>'], type='http', auth="user",
                website=True, sitemap=sitemap_event)
    def events(self, page=1, **searches):
        response = super(WebsiteEventControllerExtended, self).events()
        response.qcontext['is_account'] = True
        return response
