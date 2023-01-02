# import base64
# import json
#
# from odoo.addons.http_routing.models.ir_http import slug
# from odoo import fields, _
# from odoo import http
# from odoo.addons.portal.controllers.portal import CustomerPortal, \
#     pager as portal_pager
# from collections import OrderedDict
# from odoo.http import request, route
# from datetime import datetime, date
# from odoo.addons.website_sale.controllers.main import WebsiteSale
# from dateutil.relativedelta import relativedelta
#
#
# class Home(CustomerPortal):
#     @route('/', type='http', auth="user", website=True)
#     def index(self, **post):
#         return request.render("theme_sport_erp.sports_erp_home",
#                               {'is_home': True})
