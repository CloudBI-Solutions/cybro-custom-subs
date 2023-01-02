# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Organisation UI',
    'version': '14.0.1.0.0',
    'summary': 'Organisation User Interface',
    'sequence': 10,
    'description': """Organisation user interface tweaks""",
    'category': 'Website/Website',
    'author': "Cybrosys Techno Solutions",
    'company': "Cybrosys Techno Solutions",
    'maintainer': "Cybrosys Techno Solutions",
    'website': "https://cybrosys.com/",
    'depends': [
        'base',
        'organisation',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard.xml',
        'data/dashboard_data.xml',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
