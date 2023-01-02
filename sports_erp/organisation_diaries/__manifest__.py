{
    'name': 'Organisation Diaries',
    'version': '15.0.1.0.0',
    'author': 'Ljutzkanov Limited',
    'website': 'www.ljutzkanov.ltd',
    'description': """

    """,
    'depends': ['web_editor', 'base', 'survey', 'website', 'organisation'],
    'data': [

        'security/ir.model.access.csv',
        'data/survey_data.xml',
        # 'views/template.xml',
        # 'views/survey_templates.xml',
        'views/calculated_metric.xml',
        # 'views/portal_home.xml',
        'views/survey_question.xml',
        'views/survey_survey.xml',
        'views/metric_management.xml',
        'views/organisation.xml',
    ],
    'assets': {
        # 'web.assets_backend': [
        #     'survey_extension/static/src/js/body_map_widget.js',
        #     'survey_extension/static/src/js/survey_report.js'
        # ],
        'web.assets_frontend': [
            'organisation_diaries/static/src/js/survey_question.js',
            # 'survey_extension/static/src/js/custom.js',
            # 'survey_extension/static/src/js/survey_form.js',
            # 'survey_extension/static/src/js/survey_body_map_extension.js',
        ],
        # 'web.assets_qweb': [
        #     'survey_extension/static/src/xml/body_map_view.xml',
        #     'survey_extension/static/src/xml/survey_report.xml',
        # ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
