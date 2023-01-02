# -*- coding: utf-8 -*-

{
    'name': 'Compatibility Essentials',
    'version': '15.0.1',
    'summary': 'Compatibility Essentials',
    'description': 'Compatibility Essentials',
    'license': "AGPL-3",
    'depends': ['portal', 'website', 'website_sale', 'stock','iwesabe_website_theme'],
    'data': [
        'views/component_type_inherit.xml',
        'views/product_template_inherit.xml'
    ],
    'installable': True,
    'auto_install': False,
    'category': 'Website',
    'assets': {
        'web.assets_frontend': []
    }
}
