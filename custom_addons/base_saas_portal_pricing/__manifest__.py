{
    'name': "SAAS PRICING",
    'description': """SAAS PRICING""",
    'version': '15.0.1.0.0',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'depends': ['base', 'website'],
    'data': [
        'views/price_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'base_saas_portal_pricing/static/src/css/style.css',
            'base_saas_portal_pricing/static/src/js/saas.js',
        ],
        'web.assets_backend': [
        ],
    },
    'installable': True,
    'auto_install': False,
}
