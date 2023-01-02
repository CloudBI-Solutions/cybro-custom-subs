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


class CreditNotesFetchWizard(models.Model):
    _name = 'credit.notes.fetch.wizard'
    _inherit = ['order.fetch.wizard']
    _description = 'Credit Notes Fetch Wizard'

    def fetch_credit_notes(self):
        url = '/rest/V1/creditmemos?searchCriteria=0'
        type = 'GET'
        cr = self._cr
        order_list = self.env['magento.connector'].magento_api_call(headers={},
                                                                    url=url,
                                                                    type=type)

        try:
            self.fetch_orders()
            items = order_list['items']
            cr.execute("select magento_id from account_move "
                       " where magento_id is not null"
                       " and move_type = 'out_refund'")
            orders = cr.fetchall()
            x_orders = [items for item in orders for items in item]
            cr.execute("select TRIM(LEADING '0' FROM magento_id) as magento_id,"
                       "partner_id as partner from sale_order "
                       "where magento_id is not null")
            orders = cr.fetchall()
            debtors_acc = self.env.company.partner_id.property_account_receivable_id
            orders_dict = dict(orders)
            for rec in items:
                if rec['increment_id'] not in x_orders:
                    gst_treatment = self.env['res.partner'].browse(
                        orders_dict[str(rec['order_id'])])
                    cr_note = self.env['account.move'].create(
                        {
                            'partner_id': orders_dict[str(rec['order_id'])],
                            'l10n_in_gst_treatment':
                                gst_treatment.l10n_in_gst_treatment,
                            'move_type': 'out_refund',
                            'invoice_date': rec['created_at'],
                            'magento': True,
                            'magento_id': rec['increment_id'],
                        })
                    for item in rec['items']:
                        quantity = float(item['qty'])
                        price = float(item['price_incl_tax'])
                        cr.execute(
                            "select id from product_product "
                            "where magento_id = '%s'", (item['product_id'],))
                        product_id = cr.fetchall()
                        product = self.env['product.product'].browse(
                                                            product_id[0][0])
                        sale_acc = product.categ_id.property_account_income_categ_id
                        cr_note.invoice_line_ids.create([
                            {
                                'product_id': product_id[0][0],
                                'move_id': cr_note.id,
                                'move_name': cr_note.name,
                                'name': item['name'],
                                'date': rec['created_at'],
                                'company_id': self.env.company.id,
                                'quantity': quantity,
                                'price_unit': price,
                                'debit': quantity * price,
                                'credit': 0.0,
                                'account_id': sale_acc.id, #Local Sales
                            },
                            {
                                'move_id': cr_note.id,
                                'account_id': debtors_acc.id, #Debtors
                                'credit': quantity * price,
                                'debit': 0.0,
                                'exclude_from_invoice_tab': True,
                                'name': cr_note.name,
                                'company_id': self.env.company.id,
                            }],)
                    cr_note.action_post()

            return {
                'type': 'ir.actions.client',
                'tag': 'reload'
            }

        except Exception as e:
            _logger.info("Exception occured %s", e)
            raise exceptions.UserError(_("Error Occured %s") % e)
