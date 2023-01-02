{
    'name': "Employee Helpdesk ",
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

        'data/helpdesk_sequence.xml',
        'data/employee_helpdesk.xml',

        'views/helpdesk.xml',
        'views/helpdesk_menu.xml',

        'views/ticket_form.xml',
        'views/ticket_success.xml',
    ],
    'installable': True,

}