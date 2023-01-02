import json
import logging
import werkzeug

_logger = logging.getLogger(__name__)

from odoo import fields, http, _
from odoo.addons.survey.controllers.main import Survey
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo import http
from odoo.http import request
import base64
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError, UserError
from odoo.tools import format_datetime, format_date, is_html_empty
from odoo.http import content_disposition, dispatch_rpc, request, serialize_exception

class CustomerPortal(CustomerPortal):


    @http.route(['/my/custom_dashboards'], type='http', auth="user", website=True)
    def portal_my_custom_dashboard(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        dashboards = request.env['ks_dashboard_ninja.board'].sudo().search([('show_in_portal','=',True)])
        values = {'dashboards':dashboards}
        return request.render("dashboard_extension.portal_dashboard_line", values)

    @http.route(['/my/dashboard/<int:dashboard_id>'], type='http', auth="user", website=True)
    def portal_dashboard(self, **kwargs):
        ks_container_class_layout1 = 'grid-stack-item'
        ks_inner_container_class_layout1 = 'grid-stack-item-content'
        dashboard_id = kwargs.get('dashboard_id')
        dashboard = request.env['ks_dashboard_ninja.board'].sudo().search([('id','=',dashboard_id)])
        dashboard_data = dashboard.ks_fetch_dashboard_data(dashboard_id)
        dashboard_manager = dashboard_data.get('ks_dashboard_manager')
        dashboard_items = request.env['ks_dashboard_ninja.item'].sudo().search([('ks_dashboard_ninja_board_id','=',dashboard_id)])
        vals = {'dashboard':dashboard,'dashboard_items':dashboard_items,
                'dashboard_manager':dashboard_manager,'dashboard_data':dashboard_data,
                'ks_container_class_layout1':ks_container_class_layout1,'ks_inner_container_class_layout1':ks_inner_container_class_layout1}
        return request.render("dashboard_extension.portal_dashboard",vals)
