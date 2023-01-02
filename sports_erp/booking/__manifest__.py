# -*- coding: utf-8 -*-

{
    'name': "Booking",
    'version': "15.0.1.0.0",
    'summary': """ Booking Module """,
    'description': """ Booking Management """,
    'author': "Ljutzkanov Ltd",
    'company': "Ljutzkanov Ltd",
    'maintainer': "Ljutzkanov Ltd",
    'website': "https://www.ljutzkanov.ltd/",
    'category': 'Tools',
    'depends': ['base', 'calendar', 'crm', 'website', 'organisation'],
    'data': [
        'security/ir.model.access.csv',
        'security/booking_security.xml',
        'data/data.xml',
        'data/email_template.xml',
        'data/ir_crone.xml',
        'views/booking_views.xml',
        'views/calendar_event_views.xml',
        'views/res_config_settings_views.xml',
        'views/coach_views.xml',
        'views/product.xml',
        'views/menuitems.xml',
        # 'views/assets.xml',
        'views/dashboard_templates.xml',


    ],
    'assets': {
        'web.assets_frontend': [
            'booking/static/src/js/booking.js',
            'booking/static/src/js/booking_form_editor.js',
            'booking/static/src/css/booking.css',
        ],
    },
    'images': [],
    'license': "AGPL-3",
    'installable': True,
    'application': True
}
