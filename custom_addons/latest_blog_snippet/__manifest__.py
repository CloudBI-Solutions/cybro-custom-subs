{
    'name': "Latest Blog Snippet",
    'version': '15.0.1.0.0',
    'depends': ['base', 'website', 'website_blog'],
    'author': "Cybrosys Technologies",
    'company': "Cybrosys Technologies",
    'category': 'category',
    'description': """
    Description text
    """,
    'data': [
        'views/snippets/s_dynamic_snippet_blog.xml',
        'views/snippets/s_latest_blog_snippet_card.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'latest_blog_snippet/static/src/snippets/s_dynamic_snippet_blog/blog_snippet.js',
        ],
    },

    'installable': True,

}
