# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Athira Premanand(odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################

{
    'name': "POS Session Reports",
    'version': '15.0.1.0.0',
    'sequence': -100,
    'author': "Cybrosys Techno Solutions",
    'summary': """This Point of sales module will allow
                user to print POS Current and Closed Session Reports""",
    'description': 'POS Session Reports ',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'images': ['static/description/banner.png'],
    'website': 'https://www.cybrosys.com',
    'category': 'Point of Sale',
    'depends': ['base', 'point_of_sale'],
    'application': True,
    'data': [
                'security/ir.model.access.csv',
                'views/view_session_report.xml',
                'views/closed_session.xml',
                'views/report_action.xml',
                'wizard/wizard.xml',
                'views/menu.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'pos_z_session_reports/static/src/js/report_button.js',
            'pos_z_session_reports/static/src/js/SessionSummaryReceipt.js',
            'pos_z_session_reports/static/src/js/SessionSummaryReceiptScreen.js',
        ],
        'web.assets_qweb': [
            'pos_z_session_reports/static/src/xml/report_button.xml',
            'pos_z_session_reports/static/src/xml/SessionSummaryReceipt.xml',
            'pos_z_session_reports/static/src/xml/SessionSummaryReceiptScreen.xml',
        ],

    },
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
