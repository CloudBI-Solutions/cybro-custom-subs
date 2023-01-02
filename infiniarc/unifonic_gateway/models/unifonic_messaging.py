# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2016 Webkul Software Pvt. Ltd.
# Author : www.webkul.com
#
##############################################################################
import logging
import requests
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, _
from urllib3.exceptions import HTTPError

def send_sms_using_unifonic(body_sms, mob_no, from_mob=None, sms_gateway=None):
    '''
    This function is designed for sending sms using unifonic SMS API.
    :param body_sms: body of sms contains text
    :param mob_no: Here mob_no must be string having one or more number
     seprated by (,)
    :param from_mob: sender mobile number or id used in unifonic API
    :param sms_gateway: sms.mail.server config object for unifonic Credentials
    :return: response dictionary if sms successfully sent else empty dictionary
    '''
    if not sms_gateway or not body_sms or not mob_no:
        return {}
    if sms_gateway.gateway == "unifonic":
        AppSid = sms_gateway.unifonic_appsid
        senderID = sms_gateway.unifonic_sender_id
        values = {"AppSid":AppSid,"SenderID":senderID,"Body":body_sms,"Recipient":int  (mob_no),"baseEncode":"true"}
        headers = {
            'accept': "application/json",
            }
        try:
            response = requests.post('https://el.cloud.unifonic.com/rest/SMS/messages', data=values, headers=headers)
            return response.json()
        except HTTPError as e:
            _logger.info(
                "---------------unifonic HTTPError While Sending SMS ----%r---------", e)
            return {'error_msg':e}
        except Exception as e:
            _logger.info(
                "---------------unifonic Exception While Sending SMS -----%r---------", e)
            return {'error_msg':e}
    return {}
 

class SmsSms(models.Model):
    """SMS sending using unifonic SMS Gateway."""

    _inherit = "wk.sms.sms"
    _name = "wk.sms.sms"
    _description = "unifonic SMS"

    def send_sms_via_gateway(
            self, body_sms, mob_no, from_mob=None, sms_gateway=None):
        ctx= self._context
        self.ensure_one()
        gateway_id = sms_gateway if sms_gateway else super(
            SmsSms, self).send_sms_via_gateway(
            body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        if gateway_id:
            if gateway_id.gateway == 'unifonic':
                for element in mob_no:
                    for mobi_no in element.split(','):
                        response = send_sms_using_unifonic(
                            body_sms, mobi_no, from_mob=from_mob,
                            sms_gateway=gateway_id)
                        sms_report_obj = self.env["sms.report"].create({
                            'to': mobi_no, 'msg': body_sms,
                            'sms_sms_id': self.id,
                            "auto_delete": self.auto_delete,
                            'sms_gateway_config_id': gateway_id.id})
                        vals = {'state': 'undelivered'}
                        if response.get('success'):
                            data = response.get('data')
                            if data.get('MessageID'):
                                vals['unifonic_sms_id'] =  data.get('MessageID')
                                if data.get('Status') == 'Sent':
                                    if sms_report_obj.auto_delete:
                                        sms_report_obj.unlink()
                                    else:
                                        vals['state'] = 'delivered'
                                if data.get('Status') == 'Queued':
                                    vals['state'] = 'sent'
                        elif not response.get('success'):
                            vals.update({'state': 'failed','message':response.get('message')})
                        if sms_report_obj:
                            sms_report_obj.write(vals)
                    else:
                        self.write({'state': 'error'})
                else:
                    self.write({'state': 'sent'})
            else:
                gateway_id = super(SmsSms, self).send_sms_via_gateway(
                    body_sms, mob_no, from_mob=from_mob,
                    sms_gateway=sms_gateway)
        else:
            _logger.info(
                "------------------ SMS Gateway not found ---------------")
        return gateway_id

    def _get_partner_mobile(self, partner):
        mobile = super(SmsSms, self)._get_partner_mobile(partner)
        if self.sms_gateway_config_id.gateway == 'unifonic' and mobile.startswith('+'):
            mobile = mobile.split('+')[1]
        return mobile


class SmsReport(models.Model):
    """SMS report."""

    _inherit = "sms.report"
    unifonic_sms_id = fields.Char("unifonic SMS ID")

    def send_sms_via_gateway(
            self, body_sms, mob_no, from_mob=None, sms_gateway=None):
        self.ensure_one()
        gateway_id = sms_gateway if sms_gateway else super(
            SmsReport, self).send_sms_via_gateway(
            body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        if gateway_id:
            if gateway_id.gateway == 'unifonic':
                for element in mob_no:
                    count = 1
                    for mobi_no in element.split(','):
                        if count == 1:
                            self.to = mobi_no
                            rec = self
                        else:
                            rec = self.create({
                                'to': mobi_no, 'msg': body_sms,
                                "auto_delete": self.auto_delete,
                                'sms_gateway_config_id': gateway_id.id})
                        response = send_sms_using_unifonic(
                            body_sms, mobi_no, from_mob=from_mob,
                            sms_gateway=gateway_id)
                        vals = {'state': 'undelivered'}
                        if response.get('success'):
                            data = response.get('data')
                            if data.get('MessageID'):
                                vals['unifonic_sms_id'] =  data.get('MessageID')
                                if data.get('Status') == 'Sent':
                                    if rec.auto_delete:
                                        rec.unlink()
                                    else:
                                        vals['state'] = 'delivered'
                                if data.get('Status') == 'Queued':
                                    vals['state'] = 'sent'
                        elif not response.get('success'):
                            vals.update({'state': 'failed','message':response.get('message')})
                        if rec:
                            rec.write(vals)
                        count += 1
            else:
                gateway_id = super(SmsReport, self).send_sms_via_gateway(
                    body_sms, mob_no, from_mob=from_mob,
                    sms_gateway=sms_gateway)
        return gateway_id