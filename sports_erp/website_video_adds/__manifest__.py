# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Technologies Pvt. Ltd (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'Web Video Adds',
    'category': 'Accounting/Accounting',
    'version': '15.0.1.0.0',
    'author': 'Cybrosys',
    'summary': 'Web Video Adds',
    'description': 'Web Video Adds',
    'depends': ['base', 'website_sale'],
    'website': 'https://www.cybrosys.com/',
    'data': ['views/product_add_video.xml','views/product_add_video_viewer.xml'],
    'installable': True,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_qweb':[
            'website_video_adds/static/src/xml/product_add_video_template.xml'],
        'web.assets_backend': [
            'website_video_adds/static/src/js/product_add_video_template.js'],
    }
}
