import time
from odoo import http
from odoo.http import request


class LatestBlog(http.Controller):
    @http.route('/latest_blog_snippet/blog_snippet', type='json',
                auth='public', website=True)
    def latest_blog(self, blogs_per_slide=4):
        blogs = request.env['blog.post'].search([], order='write_date desc')
        print("blogs", blogs)
        blogs_grouped = []
        blogs_list = []
        for index, blog in enumerate(blogs, 1):
            blogs_list.append(blog)
            if index % blogs_per_slide == 0:
                blogs_grouped.append(blogs_list)
                blogs_list = []
        if any(blogs_list):
            blogs_grouped.append(blogs_list)
        print('blog_grouped', blogs_grouped)
        values = {
            'blogs': blogs_grouped,
            'num_slides': len(blogs_grouped),
            'uniqueId': 'pc-%d' % int(time.time() * 1000)
        }

        print('blogs', values)
        response = http.Response(
            template='latest_blog_snippet.s_latest_blog_snippet_card',
            qcontext=values)
        return response.render()
