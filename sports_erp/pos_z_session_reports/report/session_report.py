from datetime import datetime

from odoo import models, api


class SessionReport(models.TransientModel):
    _name = "report.pos_z_session_reports.closed_session_report_template"

    @api.model
    def _get_report_values(self, docids, data):
        """This function is used to get
        the values of closed session report"""

        report_session_name = []
        report_session_name.clear()
        report_total_sale = 0
        report_total_sale_discount = 0
        report_total_sale_tax = 0
        report_total_sale_gross_total = 0
        for rec in data.get('sessions'):
            report_session = self.env['pos.session'].browse(rec)
            report_session_name.append(report_session.name)
            session_order_ids = self.env['pos.order'].search(
                [('session_id', '=', report_session.id)])
            for i in session_order_ids:
                session_order_line_ids = self.env[
                    'pos.order.line'].search([('order_id', '=', i.id)])
                for j in session_order_line_ids:
                    report_total_sale_tax += j.price_subtotal_incl - j.price_subtotal
                    report_total_sale += j.price_subtotal
                    report_total_sale_discount += j.discount
                    report_total_sale_gross_total += j.price_subtotal_incl

            open_balance = +report_session.cash_register_balance_start
            close_balance = +report_session.cash_register_balance_end_real
            diff_balance = +report_session.cash_real_difference
            report_date = datetime.now().strftime('%Y-%m-%d')
            report_time = datetime.now().time()
            report_open_balance = open_balance
            report_cls_balance = close_balance
            report_diff_balance = diff_balance

            return {
                'report_date': report_date,
                'report_time': report_time,
                'report_open_balance': report_open_balance,
                'report_cls_balance': report_cls_balance,
                'report_diff_balance': report_diff_balance,
                'report_total_sale_tax': report_total_sale_tax,
                'report_total_sale': report_total_sale,
                'report_total_sale_discount': report_total_sale_discount,
                'report_total_sale_gross_total': report_total_sale_gross_total,
            }
