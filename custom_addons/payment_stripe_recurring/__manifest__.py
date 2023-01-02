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
  "name"                 :  "Website Payment Stripe Recurring",
  "summary"              :  """Website Payment Stripe Recurring on the base of subscription_management module """,
  "category"             :  "Payment Acquirer",
  "version"              :  "1.0.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "",
  "description"          :  """Customization: Website Payment Stripe Recurring on the base of subscription_management module  """,
  "live_test_url"        :  "",
  "depends"              :  [
                             'subscription_management',
                             'website_subscription_management',
                             'payment_stripe_checkout',
                            ],
  "data"                 :  [
                             'views/templates.xml',
                            ],
  "application"          :  True,
  "currency"             :  "USD",
  "pre_init_hook": "pre_init_check",
}
