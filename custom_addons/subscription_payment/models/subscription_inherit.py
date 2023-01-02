# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
import logging
from datetime import datetime
from odoo import api, fields, models, tools, _

# from ..models.braintree_connector import BraintreeConnector

class SaleSubscriptionInherit(models.Model):
    _inherit = "sale.subscription"
    
    braintree_payment_mode = fields.Selection([('manual','Manual'),('recurring','Recurring')],string='Payment Mode')