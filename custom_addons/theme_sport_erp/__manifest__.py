{
    'name': 'Sports ERP Theme',
    'version': '15.0.1.0.0',
    'category': 'Theme/sportERP',
    'author': 'Ljutzkanov Limited',
    'website': 'www.ljutzkanov.ltd',
    'description': """ Sport ERP Theme
    """,
    'summary': 'Sport ERP Theme',
    'depends': ['sports_erp_dashboard'],
    'data': [
        'data/website_menus.xml',
        'views/header.xml',
        'views/footer.xml',
        'views/snippet.xml',
        'views/layout.xml',
        'views/sports_erp_home.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_sport_erp/static/src/css/style.min.css',
            'theme_sport_erp/static/src/css/main.css',
            'theme_sport_erp/static/src/js/header.js',
        ],
        'web.assets_qweb': [
            # 'theme_sport_erp/static/src/xml/landing.xml',
        ],
    },

    'snippet_lists': {
        'homepage': ['s_hero_snippet', 's_feature_snippet'], },
    'images': ['static/src/images/brand/logo-color.png',
               'static/src/images/brand/hero-image.png'],
    'installable': True,
    'license': 'LGPL-3',
}
