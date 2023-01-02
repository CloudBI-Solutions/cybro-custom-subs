# -*- coding: utf-8 -*-

{
    'name': "Profiling",
    'version': "14.0.1.0.0",
    'summary': """ Profiling Module """,
    'description': """ Profiling Management """,
    'author': "Ljutzkanov Ltd",
    'company': "Ljutzkanov Ltd",
    'maintainer': "Ljutzkanov Ltd",
    'website': "https://www.ljutzkanov.ltd/",
    'category': 'Tools',
    'depends': ['base', 'organisation'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_crone.xml',
        'views/assessment_views.xml',
        'views/res_partner_views.xml',
        'views/menuitems.xml',
    ],
    'images': [],
    'license': "AGPL-3",
    'installable': True,
    'application': True
}
