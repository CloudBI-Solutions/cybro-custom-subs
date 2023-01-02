# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
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

{
    'name': 'Odoo15 Magento-2.3 Connector',
    'version': '15.0.1.0.0',
    'summary': 'Synchronize data between Odoo and Magento',
    'description': 'Synchronize data between Odoo and Magento, Magento, Magentov15, Magento Odoo, Odoo Magento, Magento Connector',
    'category': 'Extra Tools',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'sale_management', 'stock'],
    'website': 'https://cybrosys.com',
    'data': ['security/ir.model.access.csv',
             'data/magento_data.xml',
             'data/magento_sequence.xml',
             'views/views.xml',
             'views/products_view.xml',
             'views/orders_view.xml',
             'wizard/fetch_products_wiz.xml',
             'wizard/fetch_orders_wiz.xml',
             'wizard/fetch_customers_wiz.xml',
             'wizard/update_stock.xml',
             'wizard/fetch_customer_groups_wiz.xml',
             'views/customer_group_view.xml',
             'views/website_magento.xml',
             'wizard/website_wiz.xml',
             'views/shipment.xml',
             'wizard/shipment_wiz.xml',
             'wizard/fetch_credit_notes.xml',

             ],
    'assets': {
        'web.assets_backend': [
            'odoo11_magento2/static/src/css/magento_dashboard.css',
            'odoo11_magento2/static/src/js/magento_dashboard.js',
            'odoo11_magento2/static/src/js/lib/Chart.bundle.js',
                    ],
        'web.assets_qweb': [
            'odoo11_magento2/static/src/xml/magento_dashboard.xml',
                    ]},
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'price': 49,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
}

