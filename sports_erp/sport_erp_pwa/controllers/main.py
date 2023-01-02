import json
from odoo import http
from odoo.http import request


class SportERPPwa(http.Controller):
    def _get_sport_erp_icons(self, pwa_icon):
        icons = []
        all_icons = (
            request.env["ir.attachment"]
            .sudo()
            .search(
                [
                    ("url", "like", "/sport_erp_pwa/icon"),
                    (
                        "url",
                        "not like",
                        "/sport_erp_pwa/icon.",
                    ),
                ]
            )
        )
        for icon in all_icons:
            icon_size_name = icon.url.split("/")[-1].lstrip("icon").split(".")[0]
            icons.append(
                {
                    "src": icon.url,
                    "sizes": icon_size_name,
                    "type": icon.mimetype}
            )
        return icons

    def get_sport_erp_pwa(self):
        pwa_active = request.env[
            "ir.config_parameter"].sudo().get_param(
            "sport_erp_pwa.activate_pwa")
        if pwa_active:
            pwa_name = request.env[
                "ir.config_parameter"].sudo().get_param(
                "sport_erp_pwa.pwa_name")
            pwa_short_name = request.env[
                "ir.config_parameter"].sudo().get_param(
                "sport_erp_pwa.pwa_short_name")
            pwa_description = request.env[
                "ir.config_parameter"].sudo().get_param(
                "sport_erp_pwa.pwa_description")
            pwa_theme_color = request.env[
                "ir.config_parameter"].sudo().get_param(
                "sport_erp_pwa.pwa_theme_color")
            pwa_background_color = request.env[
                "ir.config_parameter"].sudo().get_param(
                "sport_erp_pwa.pwa_background_color")
            pwa_icon = (
                request.env["ir.attachment"]
                .sudo()
                .search([("url", "like", "/sport_erp_pwa/icon.")])
            )
            res = {
                    'short_name': pwa_short_name,
                    'name':  pwa_name,
                    'description': pwa_description,
                    'icons': self._get_sport_erp_icons(pwa_icon),
                    'start_url': '/my',
                    'background_color': pwa_background_color,
                    'display': 'standalone',
                    'theme_color': pwa_theme_color,
            }
            return res
        else:
            return 0

    @http.route('/manifest/webmanifest', type='http',
                auth='public', website=True, sitemap=False)
    def sport_erp_pwa_data(self):
        return request.make_response(json.dumps(
            self.get_sport_erp_pwa()),
            headers=[('Content-Type', 'application/json;charset=utf-8')])
