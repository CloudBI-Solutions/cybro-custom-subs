from odoo import fields, _
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request, route
from datetime import datetime
from collections import OrderedDict
from odoo.exceptions import UserError
import pytz
from datetime import timedelta
from datetime import timezone


class CustomerPortalDashboard(CustomerPortal):

    @route(['/my/attendance'], type='http', auth='user', website=True)
    def my_attendance(self):
        return request.render("portal_attendance.attendance_scan_page")

