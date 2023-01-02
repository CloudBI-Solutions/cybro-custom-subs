{
    "name": "Badmintoo",
    "summary": "Badmintoo Application",
    "version": "15.0.1.0.0",
    "depends": ['sports_erp_dashboard', 'survey', 'survey_extension'],
    "data": [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/badminto_assessment.xml',
        'views/menu.xml',
        'views/sidebar.xml',
        'views/badminto_assessment_template.xml',
        'views/assessment_details_template.xml',
        'views/res_config_settings.xml',
        'views/lifestyle_assessment.xml',
        'views/hr_assessment.xml',
        'views/mobility_assessment.xml',
        'views/mental_assessment.xml',
        'views/sc_assessment.xml',
        'views/aerobic_assessment.xml',
        'views/anaerobic_assessment.xml',
        'views/nutrition_assessment.xml',
    ],
        'assets': {
            'web.assets_backend': [
                'badminto/static/src/scss/color_widget.scss',
                'badminto/static/src/js/color_widget.js',
                'badminto/static/src/js/video_preview.js',
                'badminto/static/src/css/backend_video.css'
            ],
            'web.assets_frontend': [
                'badminto/static/src/css/dashboard.css',
                'badminto/static/src/css/badminto_badge.css',
                'badminto/static/src/js/remove_video.js',
                'badminto/static/src/js/add_button.js',
            ],
            'web.assets_qweb': [
                        'badminto/static/src/xml/video_preview.xml',
                    ],
    },
    "installable": True,
    "application": True,
}