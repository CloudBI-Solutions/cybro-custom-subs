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
    'name':       "SMSA Express Shipping Integration",
    'summary':       """The module allows the user to Integrate SMSA Web Services with Client Application (SECOM) with Odoo. Once integrated, the shipping method can be used on Odoo website by customers to get their orders delivered and in the Odoo backend by the user.""",
    'description':       """
                                    This is SMSA Express Shipping Integration.
                                    """,
    'live_test_url':  'http://odoodemo.webkul.com/?module=canada_post_shipping_integration',
    'author':       "Webkul Software Pvt. Ltd.",
    'website':       "https://store.webkul.com/Odoo.html",
    "license":       "Other proprietary",
    'maintainer':       'Pragyat Singh Rana',
    'category':       'Website',
    'version':       '1.0.4',
    'depends':       ['odoo_shipping_service_apps'],
    'data':       [
        'security/ir.model.access.csv',
        'views/smsa_shipping_service.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    'images':       ['static/description/Banner.gif'],
    'application':       True,
    'installable':       True,
    "price":  149,
    'currency':       'USD',
    'pre_init_hook':       'pre_init_check',
}
