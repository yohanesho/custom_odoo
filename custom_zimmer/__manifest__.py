# -*- coding: utf-8 -*-
{
    'name': "Addon Zimmer",

    'summary': """
        Addon Modification for PT. Zimmer Rattan""",

    'description': """
    """,

    'author': "Yohanes Ho",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'custom',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 
        'sale',
        'project',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views/company_view.xml',
        'views/sale_view.xml',
    ],
}