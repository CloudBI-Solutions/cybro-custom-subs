{
    'name': "Product Repair",
    'version': '15.0.1.0.0',
    'depends': ['base', 'stock', 'sale_management'],
    'author': "Cybrosys Technologies",
    'company': "Cybrosys Technologies",
    'category': 'category',
    'description': """
    Description text
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/product_repair_views.xml',
        'views/sale_order_views.xml',
        'data/product_repair_sequence.xml',
    ],

    'installable': True,

}