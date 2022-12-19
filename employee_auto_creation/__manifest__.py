# -*- coding: utf-8 -*-
{
    'name': "Employee Auto-Creation",
    'summary': """
        Employee will be crated autmatically when user is created
        """,
    'description': """
        v1.0.0
            * Adding field on res user that have some similarity with field in hr employee such as login and work email
            * Add option create employee
            * Create employee automatically followed by selected fields
            By: Galih Fikran
    """,
    'author': "Port Cities",
    'website': "http://www.portcities.net",
    'category': 'Uncategorized',
    'version': '13.0.1.0.0',
    'depends': ['contacts', 'hr'],
    'data': [
        'views/res_users_view.xml',
        'views/res_config_settings_view.xml',
    ],
}
