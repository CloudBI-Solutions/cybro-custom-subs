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
    _name = 'customer_group.fetch.wizard'
    _inherit = 'order.fetch.wizard'
    _description = 'Customer Group Fetch Wizard'

    def fetch_customer_group(self):
        PartnerObj = self.env['res.partner']
        cr = self._cr
        url = '/rest/V1/customerGroups/search?searchCriteria=0'
        type = 'GET'
        customer_group = self.env['magento.connector'].magento_api_call(headers={}, url=url, type=type)
        try:
            items = customer_group['items']

            cr.execute("select group_id from customer_group "
                       )
            g_id = cr.fetchall()
            g_ids = [i[0] for i in g_id] if g_id else []
            for i in items:
                if g_ids !=[]:
                    _logger.info("ALL IMPORTED")
                else:
                    values = {
                        'group_id': i['id'],
                        'group': i['code'],
                        'tax_class': i['tax_class_name']
                    }
                    self.env['customer.group'].sudo().create(values)

        except Exception as e:
            _logger.info("Exception occured %s", e)
            raise exceptions.UserError(_("Error Occured %s") % e)

