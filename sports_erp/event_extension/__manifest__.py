{
    'name': 'Event Extended',
    'version': '15.0.1.0.0',
    'author': 'Ljutzkanov Limited',
    'website': 'www.ljutzkanov.ltd',
    'description': """

    """,
    'depends': ['base', 'event', 'website', 'website_event', 'website_sale', 'event_sale'],
    'data': [
        'views/web_event_templates.xml',
        'views/event_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # 'event_extension/static/src/js/signature_pad.umd.js',
            # 'event_extension/static/src/js/app.js',
            # 'event_extension/static/src/js/custom.js',
            # 'event_extension/static/src/css/style.css'
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

