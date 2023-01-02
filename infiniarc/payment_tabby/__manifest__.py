# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Tabby Payment Acquirer',
    'version': '15.0.0.1',
    'category': 'Hidden',
    'description': """
This module adds a simple payment acquirer allowing to make test payments.
It should never be used in production environment. Make sure to disable it before going live.
""",
    'depends': ['payment'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_template.xml',
        'views/payment_template_view.xml',
        'views/product.xml',
        'data/payment_acquirer_data.xml',
    ],
    # 'uninstall_hook': 'uninstall_hook',
    # 'assets': {
    #     'web.assets_qweb': [
    #         '/home/cybrosys/odoo-15.0/infiniarc-main/payment_tabby/static/src/xml/tabby_warning.xml',
    #     ],
    # },
    'license': 'LGPL-3',
}
