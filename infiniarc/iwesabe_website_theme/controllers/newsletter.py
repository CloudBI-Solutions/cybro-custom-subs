from odoo import http
from odoo.http import request


class NewsLetterSubscription(http.Controller):
    @http.route('/ian/newsletter/subscribe', website=True, type='json',
                auth='public', csrf=False)
    def newsletter_subscription(self, email):
        contacts = request.env['mailing.contact'].sudo()
        list = request.env['mailing.list'].sudo().search([('id', '=', 1)])
        subscribed = contacts.search([('email_normalized', '=', email)])

        name = email.split('@')
        name2 = ''
        if ("." in name[0]):
            name1 = name[0].split('.')
            name2 = name1[0] + ' ' + name1[1]
        else:
            name2 = name[0]


        if subscribed:
            print('hello exist')
        else:
            contact_id = list.contact_ids.create({'email': email, 'subscription_list_ids': [[0, 0, {"list_id": 1},]
            ], 'name': name2})

            print('contact_id', contact_id.read())
            # contact = contact_id.subscription_list_ids.create({'list_id', '=', 1})
            # print('contract', contact)

