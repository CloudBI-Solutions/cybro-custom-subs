from odoo import http
from odoo.http import request


class HelpdeskTicket(http.Controller):
    @http.route('/ticket', type='http', auth="public", website=True)
    def helpdesk_ticket(self):
        user_id = request.env.user
        values = {
            'user_id': user_id,
        }
        return request.render("website_employee_helpdesk.ticket_form", values)

    @http.route('/create/ticket', type='http', auth="public", website=True)
    def ticket_success(self, **kw):
        # print('loo', kw)
        ticket = {
            'employee_id': kw.get('user_id'),
            'subject': kw.get('description'),
        }
        request.env['employee.helpdesk'].sudo().create(ticket)
        return request.render("website_employee_helpdesk.ticket_success")
