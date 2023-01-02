# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Technologies (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################

import logging
from odoo import models, fields, exceptions, _, api

logger = logging.getLogger(__name__)


class Shipment(models.Model):
    _name = 'shipment.shipment'

    name = fields.Char(string="Magento Shipment", readonly=True,
                       copy=False, default='Draft')

    shipment_id = fields.Char(string="Shipment")
    ship_date = fields.Date(string="Shipment Date")
    order_id = fields.Char(string="Order Id")
    related_so = fields.Many2one('sale.order',
                                 string='Related Order',
                                 )
    ship_to_name = fields.Char(string="Ship to Name")
    total_quantity = fields.Integer(String="Total Quantity")
    state = fields.Selection(selection=[
                                ('shipped', 'Shipped'),
                                ('cancel', 'Cancelled')], string='Status')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'shipment.shipment')
        return super(Shipment, self).create(vals)
