{
    'name': "Product Branding",
    'version': '15.0.1.0.0',
    'depends': ['base', 'sale', 'point_of_sale'],
    'author': "Cybrosys Technologies",
    'company': "Cybrosys Technologies",
    'category': 'category',
    'description': """
    Description text
    """,
    'data': [
        'views/product_template_views.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'product_branding/static/src/js/product_branding.js',
            'product_branding/static/src/js/product_branding_receipt.js',
        ],
        'web.assets_qweb': [
            'product_branding/static/src/xml/product_branding.xml',
            'product_branding/static/src/xml/product_branding_receipt.xml',
        ],
       },
    'installable': True,

}
