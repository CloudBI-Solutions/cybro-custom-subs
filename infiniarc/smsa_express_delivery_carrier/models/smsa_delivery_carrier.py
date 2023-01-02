# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
#################################################################################

import pdb
import logging
import requests
import binascii
import markupsafe
from xml.etree import ElementTree
from odoo import models, api, fields
from odoo.http import request
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

XML_HEADER = '''<?xml version="1.0" encoding="utf-8"?>'''
APIEND = {'api_end': 'http://track.smsaexpress.com/SeCom/SMSAwebService.asmx'}


class SmsaExpressAPI():

    def __init__(self, *args, **kwargs):
        self.smsa_test_passkey = kwargs.get('smsa_test_passkey')
        self.smsa_prod_passkey = kwargs.get('smsa_prod_passkey')
        self.smsa_service = kwargs.get('smsa_service')
        self.prod_environment = kwargs.get('prod_environment')
        self.smsa_currency = kwargs.get('smsa_currency')
        self.smsa_environment = kwargs.get('smsa_environment')

    def _get_consignee_data(self, recipient_info):
        consignee_data = {}
        consignee_data['cName'] = recipient_info.get('name', False)
        consignee_data['cntry'] = recipient_info.get('country_code', False)
        consignee_data['cCity'] = recipient_info.get('city', False)
        consignee_data['cZip'] = recipient_info.get('zip', False)
        consignee_data['cPOBox'] = recipient_info.get('po_box', False)
        consignee_data['cMobile'] = recipient_info.get('phone', False)
        consignee_data['cTel1'] = recipient_info.get('phone', False)
        consignee_data['cTel2'] = recipient_info.get('phone', False)
        consignee_data['cAddr1'] = recipient_info.get('street', False)
        consignee_data['cAddr2'] = recipient_info.get('street2', False)
        consignee_data['cEmail'] = recipient_info.get('email', False)
        return consignee_data

    def _get_shipper_data(self, shipper_info):
        shipper_data = {}
        shipper_data['sName'] = shipper_info.get('name', False)
        shipper_data['sContact'] = shipper_info.get('name', False)
        shipper_data['sAddr1'] = shipper_info.get('street', False)
        shipper_data['sAddr2'] = shipper_info.get('street2', False)
        shipper_data['sCity'] = shipper_info.get('city', False)
        shipper_data['sPhone'] = shipper_info.get('phone', False)
        shipper_data['sCntry'] = shipper_info.get('country_code', False)
        return shipper_data

    def _get_shipment_data(self, pickings, is_cod):
        shipment_data = {}
        currency_id = pickings.carrier_id.get_shipment_currency_id(
            pickings=pickings)
        currency_code = currency_id.name
        total_shipment_weight = pickings.shipping_weight
        total_cover_amount = pickings.cover_amount
        package_ids = pickings.package_ids
        shipment_data['weight'] = total_shipment_weight
        shipment_data['insrAmt'] = total_cover_amount
        shipment_data['insrCurr'] = currency_code
        shipment_data['carrValue'] = str(pickings.smsa_carrier_amount)
        shipment_data['codAmt'] = str(pickings.smsa_cod_amount) if is_cod else str(0)
        shipment_data['carrCurr'] = currency_code
        item_qty = 0
        for move_id in pickings.move_ids_without_package:
            item_qty = item_qty + move_id.quantity_done
        shipment_data['PCs'] = int(item_qty)
        return shipment_data

    def _request_header(self):
        return {'Content-Type':   'application/soap+xml'}

    def _smsa_send_request(self, request_xml):
        try:
            api_end = APIEND.get('api_end')
            _logger.info("SMSA api_end=%r==" % (api_end))
            _logger.info(">>>>>>>REQUEST >>>>>>>>>>>%s", request_xml)
            response = requests.post(
                url=api_end, data=request_xml.encode('utf-8'), headers=self._request_header())
            _logger.info(">>>>>> RESPONSE >>>>>>>>>>>>%s", response.content)
            return response
        except Exception as e:
            _logger.warning(
                "#WKDEBUG---SMSA  Exception-----%r---------" % (e))
            return dict(success=False, error_message=e)

    def _get_awb_response(self, data):
        tags = {'awb_tag': '{http://track.smsaexpress.com/secom/}'}
        root = ElementTree.fromstring(data.text)
        success = False
        error_message = []
        data = {}
        try:
            for ship_content in root.iter("{}{}".format(tags.get('awb_tag'), 'addShipResult')):
                if 'Failed' in ship_content.text:
                    error_message.append(ship_content.text)
                    success = False
                else:
                    data['AWB'] = ship_content.text
                    success = True
        except Exception as e:
            return dict(success=success, error_message=e)
        else:
            if success:
                return dict(success=success, data=data)
            else:
                return dict(success=success, error_message=error_message)

    def _get_label_response(self, data):
        tags = {'label_tag': '{http://track.smsaexpress.com/secom/}'}
        root = ElementTree.fromstring(data.text)
        success = False
        error_message = []
        data = {}
        try:
            for ship_content in root.iter("{}{}".format(tags.get('label_tag'), 'getPDFResult')):
                if 'Failed' in ship_content.text:
                    error_message.append(ship_content.text)
                    success = False
                else:
                    data['LABEL'] = ship_content.text
                    success = True
        except Exception as e:
            return dict(success=success, error_message=e)
        else:
            if success:
                return dict(success=success, data=data)
            else:
                return dict(success=success, error_message=error_message)

    def _get_cancel_response(self, data):
        tags = {'cancel_tag': '{http://track.smsaexpress.com/secom/}'}
        root = ElementTree.fromstring(data.text)
        success = False
        error_message = []
        data = {}
        try:
            for ship_content in root.iter("{}{}".format(tags.get('cancel_tag'), 'cancelShipmentResult')):
                if 'Failed' in ship_content.text:
                    error_message.append(ship_content.text)
                    success = False
                else:
                    data['CANCEL'] = ship_content.text
                    success = True
        except Exception as e:
            return dict(success=success, error_message=e)
        else:
            if success:
                return dict(success=success, data=data)
            else:
                return dict(success=success, error_message=error_message)

    def _get_rate_response(self, data):
        tags = {'rate_tag': '{http://track.smsaexpress.com/secom/}'}
        root = ElementTree.fromstring(data.text)
        success = False
        error_message = []
        data = {}
        try:
            for ship_content in root.iter("{}{}".format(tags.get('rate_tag'), 'RequestStatus')):
                if 'Failed' in ship_content.text:
                    error_message.append(ship_content.text)
                    success = False
                else:
                    for shp_cnt in root.iter("{}{}".format(
                            tags.get('rate_tag'), 'ShipCharges')):
                        data['charges'] = shp_cnt.text
                    success = True
        except Exception as e:
            return dict(success=success, error_message=e)
        else:
            if success:
                return dict(success=success, data=data)
            else:
                return dict(success=success, error_message=error_message)

    def _get_response_detail(self, data, request_for):
        if request_for == 'get_awb':
            response = self._get_awb_response(data)
            if not response.get('success'):
                raise UserError(response.get('error_message'))
            else:
                return response
        elif request_for == 'get_rate':
            response = self._get_rate_response(data)
            if not response.get('success'):
                raise UserError(response.get('error_message'))
            else:
                return response
        elif request_for == 'get_label':
            response = self._get_label_response(data)
            if not response.get('success'):
                raise UserError(response.get('error_message'))
            else:
                return response
        elif request_for == 'get_cancel':
            response = self._get_cancel_response(data)
            if not response.get('success'):
                raise UserError(response.get('error_message'))
            else:
                return response

    def _primary_error_check(self, response):
        tags = {'soap_tag':  '{http://www.w3.org/2003/05/soap-envelope}'}
        primary_success = True
        error_message = []
        try:
            if response.text == "Bad Request":
                error_message.append(response.text)
                primary_success = False
            else:
                root = ElementTree.fromstring(response.text)
                for parse_error in root.iter("{}{}".format(tags.get('soap_tag'), 'Text')):
                    error_message.append(parse_error.text)
                    primary_success = False
            return dict(success=primary_success, error_message=error_message)
        except Exception as e:
            return dict(success=False, error_message=e)

    def smsa_shipment_response(self, data, request_for):
        api_response = self._smsa_send_request(data)
        primary_response = self._primary_error_check(api_response)
        if primary_response.get('success'):
            response = self._get_response_detail(api_response, request_for)
            return response
        else:
            raise UserError(primary_response.get('error_message'))

    def _get_order_total_weight(self, order=None):
        total_weight = 0

        for item in order.order_line:
            total_weight = total_weight + \
                float(item.product_id.weight) * float(item.product_uom_qty)
        return total_weight


class SmsaDeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    @api.model
    def smsa_rate_shipment(self, order):
        response = dict(
            error_message=False,
            price=False,
            warning_message=False,
            success=True,
        )
        shipper_info = self.get_shipment_shipper_address(order=order)
        recipient_info = self.get_shipment_recipient_address(order=order)
        
        if self.prod_environment:
            config = self.wk_get_carrier_settings( ['smsa_prod_passkey', 'smsa_service', 'prod_environment'])
            config['smsa_environment'] = 'production'
            config['smsa_passkey'] = config.get('smsa_prod_passkey')
        else:
            config = self.wk_get_carrier_settings( ['smsa_test_passkey', 'smsa_service',])
            config['smsa_environment'] = 'test'
            config['smsa_passkey'] = config.get('smsa_test_passkey')

        api_obj = SmsaExpressAPI(**config)

        data = {}
        data['passKey'] = config.get('smsa_passkey', None)
        data['consignee_data'] = api_obj._get_consignee_data(recipient_info)
        data['shipper_data'] = api_obj._get_shipper_data(shipper_info)
        data['shipType'] = config.get('smsa_service', None)
        if self.is_cod:
            data['codAmt'] = order.amount_total
        else:
            data['codAmt'] = 0
        data['weight'] = api_obj._get_order_total_weight(order=order)
        render_data = dict(data=data)
        smsa_rate_data = self.env['ir.qweb']._render("smsa_express_delivery_carrier.smsa_rate", render_data)
        _logger.info("------------444-----%s", type(smsa_rate_data))
        label_response = api_obj.smsa_shipment_response(data=markupsafe.Markup(XML_HEADER)+smsa_rate_data, request_for="get_rate")
        response['price'] = label_response.get('data').get('charges')
        response['success'] = True
        if not response.get('error_message'):
            response['error_message'] = None
        if not response.get('price'):
            response['price'] = 0
        if not response.get('warning_message'):
            response['warning_message'] = None
        if not response.get('success'):
            return response
        return response

    @api.model
    def smsa_send_shipping(self, pickings):
        self.wk_validate_data(pickings=pickings)
        result = {'exact_price': 0, 'weight': 0, "date_delivery": None,
                  'tracking_number': '', 'attachments': []}
        currency_id = self.get_shipment_currency_id(pickings=pickings)
        currency_code = currency_id.name
        total_package = 0
        shipper_info = self.get_shipment_shipper_address(picking=pickings)
        shipper_info['company_name'] = pickings.company_id and pickings.company_id.name or ""
        recipient_info = self.get_shipment_recipient_address(picking=pickings)
        recipient_info['company_name'] = pickings.company_id and pickings.company_id.name or ""
        
        if self.prod_environment:
            config = self.wk_get_carrier_settings( ['smsa_prod_passkey', 'smsa_service', 'prod_environment'])
            config['smsa_environment'] = 'production'
            config['smsa_passkey'] = config.get('smsa_prod_passkey')
        else:
            config = self.wk_get_carrier_settings( ['smsa_test_passkey', 'smsa_service',])
            config['smsa_environment'] = 'test'
            config['smsa_passkey'] = config.get('smsa_test_passkey')
        
        config['smsa_currency'] = currency_code

        api_obj = SmsaExpressAPI(**config)
        package_ids = pickings.package_ids
        reference = pickings.origin
        number_of_packages = len(pickings.package_ids)
        tracking_numbers = []
        data = {}
        data['passKey'] = config.get('smsa_passkey', None)
        data['refNo'] = pickings.name
        data['sentDate'] = str(pickings.scheduled_date)
        data['idNo'] = ''
        data['consignee_data'] = api_obj._get_consignee_data(recipient_info)
        data['shipType'] = config.get('smsa_service', None)
        data['shipment_data'] = api_obj._get_shipment_data(pickings, self.is_cod)
        data['shipper_data'] = api_obj._get_shipper_data(shipper_info)
        render_data = dict(data=data)
        smsa_shipment_data = self.env['ir.qweb']._render(
            "smsa_express_delivery_carrier.smsa_shipment", render_data)
        awb_response = api_obj.smsa_shipment_response(
            data=markupsafe.Markup(XML_HEADER)+smsa_shipment_data, request_for="get_awb")
        result['tracking_number'] = awb_response.get('data').get('AWB')
        label_data = {
            'awbNo': result['tracking_number'],
            'passKey': data['passKey']
        }
        smsa_lable_data = self.env['ir.qweb']._render(
            "smsa_express_delivery_carrier.smsa_label", label_data)
        label_response = api_obj.smsa_shipment_response(
            data=markupsafe.Markup(XML_HEADER)+smsa_lable_data, request_for="get_label")
        result['attachments'] = [('SMSA' + str(result['tracking_number']) +
                                  '.pdf', binascii.a2b_base64(label_response.get('data').get('LABEL')))]
        return result

    @api.model
    def smsa_get_tracking_link(self, pickings):
        for obj in self:
            tnt_tracking_link = 'http://www.smsaexpress.com/Track.aspx?tracknumbers='
            return tnt_tracking_link+pickings.carrier_tracking_ref

    @api.model
    def smsa_cancel_shipment(self, pickings):
        for obj in self:
            obj.wk_validate_data(pickings=pickings)
            currency_id = self.get_shipment_currency_id(pickings=pickings)
            currency_code = currency_id.name
            config = self.wk_get_carrier_settings(
                ['smsa_test_passkey', 'smsa_prod_passkey', 'smsa_service', 'prod_environment'])
            config['smsa_currency'] = currency_code
            if config['prod_environment']:
                config['smsa_environment'] = 'production'
                config['smsa_passkey'] = config.get('smsa_prod_passkey')
            else:
                config['smsa_environment'] = 'test'
                config['smsa_passkey'] = config.get('smsa_test_passkey')

            cancel_data = {
                'awbNo':   pickings.carrier_tracking_ref,
                'passkey': config['smsa_passkey'],
                'reas': 'SMSA Cancel Shipment',
            }

            api_obj = SmsaExpressAPI(**config)
            smsa_cancel_data = self.env['ir.qweb']._render(
                "smsa_express_delivery_carrier.smsa_cancel", cancel_data)
            cancel_response = api_obj.smsa_shipment_response(
                data=markupsafe.Markup(XML_HEADER)+smsa_cancel_data, request_for="get_cancel")
            if 'Success Cancellation' in cancel_response.get('data').get('CANCEL'):
                return True
            else:
                raise UserError("SMSA Shipment unable to cancel !!!")

    @api.model
    def smsa_get_return_label(self, pickings, tracking_number, origin_date):
        raise ValidationError(
            'Return not allowed by SMSA carrier.')
