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
  "name"                 :  "Subcripton Braintree Payment ",
  "summary"              :  """Integrate Braintree Payment with Odoo subscription. """,
  "category"             :  "Website",
  "version"              :  "1.5.1",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/",
  "description"          :  """""",
  "live_test_url"        :  "https://webkul.com/blog/odoo-website-braintree-payment-acquirer/",
  "depends"              :  ['payment_braintree','sale_subscription'],
  "data"                 :  [
      'views/sale_subscription.xml'
                             
                            ],
  "application"          :  True,
  "installable"          :  True,
  
}
