{
    'name': "Session Discount",
    'version': '15.0.1.0.0',
    'depends': ['base', 'sale_management', 'point_of_sale'],
    'author': "Cybrosys Technologies",
    'company': "Cybrosys Technologies",
    'category': 'category',
    'description': """
    Description text
    """,
    'data': [
        'views/pos_config_views.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'session_discount/static/src/js/session_discount.js']
    },
    'installable': True,

}
