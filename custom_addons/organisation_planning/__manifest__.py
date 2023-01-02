# -*- coding: utf-8 -*-

{
    'name': "Project Planning",
    'summary': "Schedule and track organisations operations",
    'description': """
                    Organisation Project Planning
                    =========================
                    This module adds the features needed for an Organisation's project planning.
                    It installs the following apps:
                    - Project
                    - Timesheet""",
    'author': "Ljutzkanov Ltd",
    'company': "Ljutzkanov Ltd",
    'maintainer': "Ljutzkanov Ltd",
    'website': "https://www.ljutzkanov.ltd/",
    'category': 'Tools',
    'sequence': 170,
    'version': '15.0.1.0.0',
    'depends': ['organisation', 'project', 'sh_all_in_one_pms'],
    'data': [
        'security/planning_security.xml',
        'views/project_task_views.xml',
        'views/menu_items.xml',
        'views/sh_task_cl.xml'
    ],
    'images': [],
    'license': "AGPL-3",
    'installable': True,
    'application': True
}
