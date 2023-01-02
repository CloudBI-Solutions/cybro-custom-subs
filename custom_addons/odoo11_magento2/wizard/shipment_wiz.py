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

from odoo import models, exceptions, _

_logger = logging.getLogger(__name__)


class CustomerGroupFetchWizard(models.Model):
    _name = 'shipment.fetch.wizard'
    _inherit = 'order.fetch.wizard'
    _description = 'Shipment Fetch Wizard'

    def fetch_shipments(self):
        PartnerObj = self.env['res.partner']
        cr = self._cr
        url = '/rest/default/V1/shipments?searchCriteria=0'
        type = 'GET'
        customer_group = self.env['magento.connector'].magento_api_call(headers={}, url=url, type=type)
        try:
            self.fetch_orders()
            g_id = []
            items = customer_group['items']
            cr.execute("select shipment_id from shipment_shipment")
            g_id_dict = cr.dictfetchall()
            for rec in g_id_dict:
                g_id.append(rec['shipment_id'])
            for i in items:
                if i['increment_id'] not in g_id:
                    partner = self.env['res.partner'].search([
                        ('magento_id', '=', i['customer_id'])])
                    related_so = self.env['sale.order'].search([
                        ('magento_id', '=', i['increment_id'])
                    ])
                    values = {
                        'shipment_id': i['increment_id'],
                        'ship_date': i['created_at'],
                        'order_id': i['order_id'],
                        'ship_to_name': partner.name,
                        'related_so': related_so.id,
                        'total_quantity': i['total_qty'],
                        'state': 'shipped'
                    }
                    self.env['shipment.shipment'].sudo().create(values)
            _logger.info("ALL IMPORTED")
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }




        except Exception as e:
            _logger.info("Exception occured %s", e)
            raise exceptions.UserError(_("Error Occured %s") % e)

