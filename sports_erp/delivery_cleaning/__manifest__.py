# -*- coding: utf-8 -*-
{
    'name': 'Delivery Cleaning',
    'version': '15.0.1.0',
    'summary': 'Delivery Cleaning',
    'sequence': 4,
    'description': """Delivery Cleaning""",
    'category': 'Inventory',
    'website': 'https://www.cybrosys.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/menu_item.xml',
        'wizard/delivery_cleaning_wiz.xml',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
