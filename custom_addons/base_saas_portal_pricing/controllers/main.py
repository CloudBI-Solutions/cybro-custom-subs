from odoo import http
from odoo.http import request


class SaasPricing(http.Controller):
    @http.route('/my/pricing/', type='http', auth="public", website=True)
    def pricing(self):
        values = {}
        apps = request.env['ir.module.module'].search([
            ('application', '=', True)
        ])
        values.update({
            'apps': apps
        })
        response = request.render(
            "base_saas_portal_pricing.saas_portal_pricing", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
