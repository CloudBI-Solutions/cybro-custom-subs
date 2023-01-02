# -*- coding: utf-8 -*-

{
    'name': "Organisation Registers",
    'version': "15.0.1.0.0",
    'summary': """ Organisation Registers""",
    'description': """ Organisation Registers""",
    'author': "Ljutzkanov Ltd",
    'company': "Ljutzkanov Ltd",
    'maintainer': "Ljutzkanov Ltd",
    'website': "https://www.ljutzkanov.ltd/",
    'category': 'Tools',
    'depends': ['base', 'organisation', 'sports_erp_dashboard'],
    'data': [
        'security/ir.model.access.csv',
        'data/registers_data.xml',
        'views/athlete_group.xml',
        'views/group_template.xml',
        'views/dashboard.xml',
        'views/registers_template.xml',
        'views/registers.xml',
        'reports/registers_report_template.xml',
        'reports/registers_report.xml',

    ],
    'assets': {
        # 'web.assets_backend': [
        #     'organisation/static/src/xml/assets_backend.xml',
        #     'organisation/static/src/css/backend.css',
        # ],
        'web.assets_frontend': [
            'organisation_registers/static/src/js/group.js',
            # 'organisation/static/src/css/organisation.css',
            # 'organisation/static/src/js/website_sale.js',
        ],
    },
    # 'qweb': [
    #     'static/src/xml/attendance.xml'
    # ],
    'images': [],
    'license': "AGPL-3",
    'installable': True,
    'application': True
}
