{
    'name': "QR Code",
    'version': '15.0.1.0.0',
    'depends': ['base', 'website'],
    'author': "Cybrosys Technologies",
    'company': "Cybrosys Technologies",
    'category': 'category',
    'description': """
    Description text
    """,
    'data': [
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'qr_code/static/src/js/qr_code.js',
            ],
        'web.assets_qweb': [
            'qr_code/static/src/xml/qweb.xml'
        ],
    },
    'installable': True,
}
