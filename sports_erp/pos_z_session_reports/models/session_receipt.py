# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Athira Premanand(odoo@cybrosys.com)
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

from odoo import models, api


class SessionReceipt(models.AbstractModel):
    _name = "report.pos_z_session_reports.print_pos_session_report"

    @api.model
    def _get_report_values(self, docids, data):
        """Get session wise report"""
        where = """"""
        if docids is None:
            docids = data['docids']
        if len(docids) > 1:
            where += """ And pos_order.session_id = %s""" % (str(tuple(docids)))
            sessions = self.env['pos.session'].sudo().browse(
                docid for docid in docids)
        else:
            where += """ And pos_order.session_id = %s""" % docids[0]
            sessions = self.env['pos.session'].sudo().browse(docids[0])
        session_summary = []
        if sessions:
            for session in sessions:
                session = self.env['pos.session'].search(
                    [('id', '=', session.id)])
                order_ids = session.order_ids
                if order_ids:
                    self.env.cr.execute(
                        """
                        SELECT product.id, template.name, product.default_code
                         as code, sum(qty) as qty, 
                         sum(line.price_subtotal_incl) as total
                        FROM product_product AS product,
                            pos_order_line AS line, product_template AS template
                        WHERE product.id = line.product_id
                         AND template.id = product.product_tmpl_id
                           AND line.order_id IN %s
                        GROUP BY product.id, template.name,
                         template.default_code
                               """, (tuple(order_ids.ids),))
                    product_summary = self.env.cr.dictfetchall()
                    payment_ids = self.env["pos.payment"].search(
                        [('pos_order_id', 'in', order_ids.ids)]).ids
                    if payment_ids:
                        self.env.cr.execute("""
                           SELECT method.name, sum(amount) total
                           FROM pos_payment AS payment,
                                pos_payment_method AS method
                           WHERE payment.payment_method_id = method.id
                               AND payment.id IN %s
                           GROUP BY method.name
                                               """, (tuple(payment_ids),))
                        payments_summary = self.env.cr.dictfetchall()
                    else:
                        payments_summary = []
                else:
                    product_summary = []
                    payments_summary = []

                session = self.env['pos.session'].search(
                    [('id', '=', session.id)])
                orders = session.order_ids
                categories = []
                discount = []
                if orders:
                    self.env.cr.execute("""
                    SELECT category.name, sum(price_subtotal_incl) as amount, 
                   sum(qty) as qty FROM pos_order_line AS line INNER JOIN
                   product_product AS product ON 
                   line.product_id = product.id INNER JOIN
                   product_template AS template ON 
                   product.product_tmpl_id = template.id 
                   INNER JOIN pos_category as category ON 
                   template.pos_categ_id = category.id 
                   WHERE line.order_id IN %s GROUP BY category.name """,
                                        (tuple(orders.ids),))
                    categories = self.env.cr.dictfetchall()

                    self.env.cr.execute("""
                    select sum(
                    (posl.qty * posl.price_unit) - posl.price_subtotal_incl)
                     as discount,
                   sum(posl.price_subtotal_incl) as gross_sale
                   from pos_order join pos_order_line as posl
                    on posl.order_id = pos_order.id
                    where pos_order.session_id = %d""" % session.id)
                    discount = self.env.cr.dictfetchall()
                session_summary.append({
                    'session_name': session.name,
                    'start_date': session.start_at,
                    'end_date': session.stop_at,
                    'opening_balance': session.cash_register_balance_start,
                    'closing_balance': session.cash_register_balance_end_real,
                    'product_summary': product_summary,
                    'payments_summary': payments_summary,
                    'difference': session.cash_real_difference,
                    'session_status': dict(
                        session._fields['state'].selection).get(session.state),
                    'categories': categories,
                    'discount': discount[0]['discount'] if discount else 0.0,
                    'gross_sale': discount[0]['gross_sale'] if discount else 0.0
                })
        return {'session_summaries': session_summary}
