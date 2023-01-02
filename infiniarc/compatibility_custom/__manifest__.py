# -*- coding: utf-8 -*-

{
    'name': 'Compatibility Customizations',
    'version': '15.0.1',
    'summary': 'Compatibility Customizations',
    'description': 'Compatibility Customizations',
    'license': "AGPL-3",
    'depends': ['portal', 'website', 'website_sale', 'stock'],
    'data': [
        'views/socket_type.xml',
        'views/filter.xml',
        'views/models.xml',
        'views/gpu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'category': 'Website',
    'assets': {
        'web.assets_frontend': []
    }
}
