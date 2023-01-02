import json
from odoo import http
from odoo.http import request


class BasePwa(http.Controller):
    def pwa_data(self):
        pwa_enable = request.env[
            "ir.config_parameter"].sudo().get_param(
            "base_pwa.pwa_enable")
        if pwa_enable:
            res = {
                'short_name': request.env[
                                "ir.config_parameter"].sudo().get_param(
                                "base_pwa.pwa_short_name"),
                'name': request.env[
                                "ir.config_parameter"].sudo().get_param(
                                "base_pwa.pwa_name"),
                'description': request.env[
                                "ir.config_parameter"].sudo().get_param(
                                "base_pwa.pwa_description"),
                'icons': [
                    {
                        'src': 'http://localhost:8016/web/content/242',
                        'type': 'image/png',
                        'sizes': '144x144',
                        'purpose': 'any maskable'
                    },
                ],
                'start_url': request.env[
                            "ir.config_parameter"].sudo().get_param(
                            "base_pwa.pwa_start_link"),
                'background_color': request.env[
                            "ir.config_parameter"].sudo().get_param(
                            "base_pwa.pwa_background_color"),
                'display': 'standalone',
                'theme_color': request.env[
                            "ir.config_parameter"].sudo().get_param(
                            "base_pwa.pwa_theme_color"),
            }
            print(res)
            return res

    @http.route('/manifest/webmanifest', type='http',
                auth='public', website=True, sitemap=False)
    def base_pwa_data(self):
        return request.make_response(
            json.dumps(self.pwa_data()),
            headers=[('Content-Type', 'application/json;charset=utf-8')])
