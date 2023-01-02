from datetime import date

from odoo import SUPERUSER_ID, _, http
from odoo.http import request


class MapValueController(http.Controller):

    @http.route('/map_value', type="json", auth="none")
    def map_value(self, outlet_id, **kwargs):
        company_outlets_id = request.env['company.outlets'].sudo().browse(int(outlet_id))
        address = company_outlets_id.street + ' ' + company_outlets_id.city + ' ' + company_outlets_id.state_id.name + ' ' + company_outlets_id.country_id.name
        outlet_address = company_outlets_id.street
        outlet_city = company_outlets_id.city
        outlet_zip = company_outlets_id.zip
        city = outlet_city + ' ' + outlet_zip
        print('addr', address)
        print('addr1', outlet_address)
        print('addr2', city)

        return {
            'address': address,
            'outlet': outlet_address,
            'city': city,
        }
