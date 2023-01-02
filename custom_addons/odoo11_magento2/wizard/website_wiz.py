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

from odoo import models,fields, exceptions, _

_logger = logging.getLogger(__name__)


class WebsiteFetchWizard(models.Model):
    _name = 'website.fetch.wizard'
    _description = 'Website Fetch Wizard'

    website_fetch_type = fields.Selection([('website', 'Fetch magento websites'),
                                          ('stores', 'Fetch Magento stores')],
                                         string="Operation Type")

    def fetch_website(self):
        """Fetch products"""
        if self.website_fetch_type == 'website':
            self.fetch_websites()

        elif self.website_fetch_type == 'stores':
            self.fetch_stores()

    def fetch_websites(self):
        url = '/rest/V1/store/websites'
        type = 'GET'
        magento_websites = self.env['magento.connector'].magento_api_call(headers={}, url=url, type=type)
        try:
            items = magento_websites
            for i in items:
                values={
                    'website_name':i['name'],
                    'website_code':i['code'],
                    'default_store':i['default_group_id']
                }
                print("values", values)
                self.env['website.magento'].sudo().create(values)




        except Exception as e:
            _logger.info("Exception occured %s", e)
            raise exceptions.UserError(_("Error Occured %s") % e)

    def fetch_stores(self):
        url = '/rest/default/V1/store/storeViews'
        type = 'GET'
        magento_stores = self.env['magento.connector'].magento_api_call(headers={}, url=url, type=type)
        print("mm", magento_stores)
        try:
            items = magento_stores
            for i in items:
                values = {
                    'store_name': i['name'],
                    'store_code': i['code'],
                    'default_website': i['website_id']
                }
                print("values", i)
                self.env['stores.magento'].sudo().create(values)

        except Exception as e:
            _logger.info("Exception occured %s", e)
            raise exceptions.UserError(_("Error Occured %s") % e)
