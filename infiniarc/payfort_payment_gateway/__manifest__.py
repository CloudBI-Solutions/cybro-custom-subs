{
    'name': 'Payfort Payment Gateway Integration',
    'version': '15.0.0.0',
    'summary': 'Payfort Payment Acquirer',
    'description': 'Payfort Payment Acquirer',
    'depends': ['payment'],
    'category': 'Accounting/Payment Acquirers',
    'data': [
        'views/payment_payfort_template.xml',
        'views/request_view.xml',
        'views/payfort_acquirer.xml',
        'data/data.xml',
    ],
    'application': True,
    'license': 'LGPL-3',

}
