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
{
  "name"                 :  "Unifonic SMS Gateway",
  "summary"              :  """Odoo Unifonic SMS Gateway integrates Unifonic SMS Gateway to Odoo. Hence, you can send SMS directly from Odoo to your partners' mobile phone via Unifonic SMS Gateway. It facilitates you to send SMS to your customers, suppliers or anyone.""",
  "category"             :  "Marketing",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com",
  "description"          :  """ Odoo Unifonic SMS Gateway
Unifonic SMS Gateway in Odoo
Integrate SMS Gateways with Odoo
Click Send SMS Gateway
Bulk SMS send
Send Bulk SMS
Mobily SMS alert
Use Netelip in odoo
Skebby communication
Mobily odoo
Click Send
Odoo SMS Notification
Send Text Messages to mobile
Integrate SMS Gateways with Odoo
SMS Gateway
SMS Notification
Notify with Odoo SMS
Mobile message send
Send Mobile messages
Mobile notifications to customers
Mobile Notifications to Users
How to get SMS notification in Odoo
module to get SMS notification in Odoo
SMS Notification app in Odoo
Notify SMS in Odoo
Add SMS notification feature to your Odoo
Mobile SMS feature
How Odoo can help to get SMS notification,
Odoo SMS OTP Authentication,
Marketplace SMS
Plivo SMS Gateway
ClickSend SMS Gateway
Skebby SMS Gateway
Mobily SMS Gateway
MSG91 SMS Gateway
Twilio SMS Gateway
Netelip SMS Gateway
Messagebird SMS Gateway
Textlocal SMS Gateway""",
  "depends"              :  ['sms_notification'],
  "data"                 :  [
                             'views/unifonic_config_view.xml',
                             'views/sms_report.xml',
                            ],
  "images"               :  ['static/description/Banner.gif'],                          
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}
