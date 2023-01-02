# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################
import logging
from odoo import api, fields, models, _
from odoo.tools import float_is_zero
import datetime

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class Subscription(models.Model):

    _inherit = "subscription.subscription"
    _description = "Subscription Inherit"

    payment_token_id = fields.Many2one('payment.token', "Stripe Payment Token")
    payment_transections = fields.One2many('payment.transaction','subscription_id','Recurring Payment Reference')

    def _set_payment_token(self,subscription):
        try:
            order_id = subscription.so_origin[0]
            invoice_ids =  order_id.invoice_ids if order_id else subscription.invoice_ids
            last_tx = False
            all_done_tx = self.env['payment.transaction'].search([('provider','=', 'stripe_checkout'),('state','=','done'),('partner_id','=',order_id.partner_id.id)])
            for invoice_id in invoice_ids:
                last_tx = all_done_tx.filtered(lambda tx: invoice_id in tx.invoice_ids)
                if last_tx:
                    subscription.payment_token_id = last_tx.payment_token_id
                    break
        except Exception as e:
            _logger.info('\n----Strip Recurring  Error: While getiing the payment token   ---%r--------',str(e))


    @api.model
    def create_automatic_invoice(self):
        subscriptions = self.env['subscription.subscription'].search(
            [('start_date', '<=', fields.Datetime.now()),
             ('state', '=', 'in_progress'),
             ('next_payment_date', '<=', fields.Datetime.now())])
        for subscription in subscriptions:
            if not subscription.payment_token_id:
                self._set_payment_token(subscription)
            if subscription.payment_token_id:
                subscription.action_invoice_recurring_stripe_payment(),
            else:
                subscription.action_invoice_create()

    def action_invoice_create(self, grouped=False, final=False):
        if self.payment_token_id:
            return self.action_invoice_recurring_stripe_payment()
        else:
            return super(Subscription, self).action_invoice_create(grouped=grouped,final=final)

    def action_invoice_recurring_stripe_payment(self, grouped=False, final=False):
        inv_obj = self.env['account.move']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        invoices = {}
        for subscription in self:
            if not subscription.active:
                # raise UserError(_("You can't generate invoice of an Inactive Subscription."))
                _logger.info("........Stripe Recurring...Error : You can't generate invoice of an Inactive Subscription.")
            if subscription.state == 'draft':
                _logger.info("........Stripe Recurring...Error : You can't generate invoice of a subscription which is in draft state, please confirm it first.")
                # raise UserError("You can't generate invoice of a subscription which is in draft state, please confirm it first.")
            if subscription.trial_period:
                if subscription.start_date > datetime.today().date():
                    _logger.info("........Stripe Recurring...info : You can't create invoice for this subscription because, its in a trial period.")
            if subscription.num_billing_cycle == subscription.invoice_count or subscription.num_billing_cycle < subscription.invoice_count and subscription.num_billing_cycle != -1:
                subscription.state = 'expired'
                _logger.info("........Stripe Recurring...info :  Subscription has been expired.")
                return True
            group_key = subscription.id if grouped else (subscription.customer_name.id, subscription.product_id.currency_id.id)
            if float_is_zero(subscription.quantity, precision_digits=precision):
                    continue
            if group_key not in invoices:
                inv_data = subscription._prepare_invoice()
            elif group_key in invoices and subscription.name not in invoices[group_key].so_origin.split(', '):
                invoices[group_key].write({'origin': invoices[group_key].origin + ', ' + subscription.name})
            if subscription.quantity > 0:
                invoice_lines = subscription.invoice_line_create(inv_data,subscription.quantity)
                invoice = inv_obj.create(invoice_lines)
                invoices[group_key] = invoice

        if invoices:
            message = 'Invoice Created'
            invoice_generated = self.env["ir.default"].get('res.config.settings', 'invoice_generated')
            sent_invoice = self.env["ir.default"].get('res.config.settings', 'invoice_email')

            for inv in invoices.values():
                pass
                # if self.invoice_ids:
                #     self.invoice_ids = [(4, inv.id)]
                # else:
                #     self.invoice_ids = [inv.id]
                # invoice.make_payment(invoice_generated)
            invoice._post()
                                   
            res = self._stripe_checkout_do_s2s_payment(invoice)
            if res['status'] and res['response'].get('status') == 'succeeded':
                self.settle_invoice(invoice, sent_invoice, state="paid")
                start_date = datetime(year=self.start_date.year, month=self.start_date.month, day=self.start_date.day, minute=0, hour=0, second=0) if self.source =='manual' else self.start_date + relativedelta(days = 1)
                if not isinstance(start_date, datetime):
                    start_date = datetime(*start_date.timetuple()[:6])
                if subscription.num_billing_cycle != subscription.invoice_count:
                    if self.num_billing_cycle > 0:
                        end_date = datetime(year=self.end_date.year, month=self.end_date.month, day=self.end_date.day, minute=0, hour=0, second=0)
                        date_intervals = self.cal_date_period(start_date, end_date, self.num_billing_cycle)
                        self.next_payment_date = datetime.strptime(date_intervals[self.invoice_count-1], "%d/%m/%Y %H:%M:%S")
                    else:
                        end_date = start_date if not self.next_payment_date else self.next_payment_date
                        if self.unit == 'day':
                            end_date = end_date + relativedelta(days=self.duration)
                        if self.unit == 'month':
                            end_date = end_date + relativedelta(months=self.duration)
                        if self.unit == 'year':
                            end_date = end_date + relativedelta(years=self.duration)
                        if self.unit == 'week':
                            end_date = end_date + timedelta(weeks=self.duration)
                        self.next_payment_date = end_date
                else:
                    self.next_payment_date = self.end_date
            else:
                self.settle_invoice(invoice, sent_invoice, state="post")
                # start_date = datetime(year=self.start_date.year,
                #                       month=self.start_date.month,
                #                       day=self.start_date.day, minute=0, hour=0,
                #                       second=0) if self.source == 'manual' else\
                #     self.start_date + relativedelta(days=1)
                # if not isinstance(start_date, datetime):
                #     start_date = datetime(*start_date.timetuple()[:6])
                # if subscription.num_billing_cycle != subscription.invoice_count:
                #     if self.num_billing_cycle > 0:
                #         end_date = datetime(year=self.end_date.year, month=self.end_date.month, day=self.end_date.day, minute=0, hour=0, second=0)
                #         date_intervals = self.cal_date_period(start_date, end_date, self.num_billing_cycle)
                #         self.next_payment_date = datetime.strptime(date_intervals[self.invoice_count-1], "%d/%m/%Y %H:%M:%S")
                #     else:
                #         end_date = start_date if not self.next_payment_date else self.next_payment_date
                #         if self.unit == 'day':
                #             end_date = end_date + relativedelta(days=self.duration)
                #         if self.unit == 'month':
                #             end_date = end_date + relativedelta(months=self.duration)
                #         if self.unit == 'year':
                #             end_date = end_date + relativedelta(years=self.duration)
                #         if self.unit == 'week':
                #             end_date = end_date + timedelta(weeks=self.duration)
                #         self.next_payment_date = end_date
                # else:
                #     self.next_payment_date = self.end_date
                _logger.info("..................Unable to do recurring payment................%r...............",res)
            return res

    def settle_invoice(self, invoice, sent_invoice, state='post'):
        # invoice._post()
        invoice._compute_amount()
        message = state + "Post Invoice Created"
        if sent_invoice:
            template = self.env.ref('account.email_template_edi_invoice')
            subjects = self.env['mail.template']._render_template(template.subject, 'account.move', invoice.ids)
            body = template._render_template(template.body_html, 'account.move', invoice.ids)
            emails_from = self.env['mail.template']._render_template(template.email_from,'account.move', invoice.ids)
            mail_compose_obj = self.env['mail.compose.message'].create({
                'subject':subjects,
                'body':body,
                'parent_id':False,
                'email_from':emails_from,
                'model':'account.move',
                'res_id':invoice.id,
                'record_name':invoice.name,
                'message_type':'comment',
                'composition_mode':'comment',
                'partner_ids':[invoice.partner_id.id],
                'auto_delete':False,
                'template_id':template.id,
                'add_sign':True,
                'subtype_id':1,
                'author_id':self.env.user.partner_id.id,
            })
            mail_compose_obj.with_context(custom_layout="mail.mail_notification_paynow",model_description='invoice').send_mail()
            self.mapped('invoice_ids').write({'invoice_sent': True})

    def _stripe_checkout_do_s2s_payment(self,invoice):
        acquirer_id = self.env['payment.acquirer'].search([('provider','=','stripe_checkout')], limit=1)
        order_id = order_id = self.so_origin
        reference_values = order_id and {'sale_order_ids': [(4, order_id)]} or {}
        reference = self.env['payment.transaction']._compute_reference(values=reference_values, prefix=self.name)
        token=self.payment_token_id
        values = {
            'acquirer_id': int(acquirer_id),
            'reference': reference,
            'type': 'server2server',
            'payment_token_id': int(token) if token else None,
            'return_url': '/shop/payment/validate',
        }
        tx =  invoice and invoice._create_payment_transaction(values) or False
        if tx:
            self.payment_transections = [(4,tx.id)]
            res = tx._stripe_checkout_do_s2s_payment()
        else:
            _logger.info("\nunable to create Tx for"
                         " _stripe_checkout_do_s2s_payment")
            res = {'status': False}
        return res
