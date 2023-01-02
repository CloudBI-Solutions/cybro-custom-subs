# -*- coding: utf-8 -*-
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo import fields, http, _
from odoo.http import request
import io, base64
from PIL import Image
import urllib

class WebsiteEventControllerExtended(WebsiteEventController):

    @http.route(['''/event/registration/new_event'''],
                type='http', auth="public",
                methods=['POST'], website=True)
    def registration_new_event(self, **post):
        print(post, "posttttt")
        data = post.get('signature').split(',')
        print(post)
        imgdata = bytes(data[1], 'utf-8')

        limit = post.get('reg_no')
        tick_temp = post.get('user_ticket_ids')
        temp_tick = tick_temp.split('],')
        res = [i.strip("[]").split(", ") for i in temp_tick]
        ticket_ids = []
        for i in res:
            for j in i:
                t_id = j.split(',')
                t_val = list(map(int, t_id))
                ticket_ids.append(t_val)
        visitor_sudo = request.env[
            'website.visitor']._get_visitor_from_request(force_create=True)
        visitor_sudo._update_visitor_last_visit()
        u_name = post.get('user_name').split(',')
        user_names = list(map(str, u_name))
        u_email = post.get('user_email').split(',')
        user_emails = list(map(str, u_email))
        u_phone = post.get('user_phone').split(',')
        user_phones = list(map(str, u_phone))
        u_dob = post.get('user_dob').split(',')
        user_dob = list(map(str, u_dob))
        u_med_info = post.get('user_med_info').split(',')
        user_med_info = list(map(str, u_med_info))
        event_id = post.get('event')
        event = request.env['event.event'].browse(event_id)
        print(event, "event....")
        order = request.website.sale_get_order(force_create=1)
        for i in range(0, int(limit)):
            for j in range(0, len(ticket_ids[i])):
                if ticket_ids[i][j] != 0:
                    ticket_id = request.env[
                        'event.event.ticket'].sudo().search(
                        [('id', '=', ticket_ids[i][j])])
                    print("test")
                    cart_values = order.with_context(
                        event_ticket_id=ticket_id.id,
                        fixed_price=True)._cart_update(
                        product_id=ticket_id.product_id.id, add_qty=1)
                    request.env['event.registration'].sudo().create({
                        'event_id': event.id,
                        'partner_id': visitor_sudo.partner_id.id,
                        'name': user_names[i],
                        'email': user_emails[i],
                        'phone': user_phones[i],
                        'dob': user_dob[i],
                        'medical_info': user_med_info[i],
                        'parent_name': post.get('parent_name'),
                        'parent_email': post.get('parent_email'),
                        'parent_phone': post.get('parent_phone'),
                        'emergency_contact_number_1': str(
                            post.get('emergency_no_1')),
                        'emergency_contact_number_2': str(
                            post.get('emergency_no_2')),
                        'signature': imgdata,
                        'event_ticket_id': ticket_ids[i][j],
                        'visitor_id': visitor_sudo.id,
                        'sale_order_id': order.id,
                        'sale_order_line_id': cart_values.get('line_id')
                    })

        return request.redirect("/shop/checkout")






