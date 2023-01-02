# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Subscription in Organisation',
    'version': '14.0.1.0.0',
    'summary': 'Subscription in Organisation',
    'sequence': 10,
    'description': """Subscription in Organisation""",
    'category': 'Website/Website',
    'author': "Cybrosys Techno Solutions",
    'company': "Cybrosys Techno Solutions",
    'maintainer': "Cybrosys Techno Solutions",
    'website': "https://cybrosys.com/",
    'depends': [
        'base',
        'organisation', 'subscription_management'
    ],
    'data': [
        'views/athletes.xml',
        'views/coaches.xml',
        'views/parents.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}
