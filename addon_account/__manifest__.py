# -*- coding: utf-8 -*-
{
    'name': "Addon Account",

    'summary': """
        Addon Custom for module Accounting & Invoicing""",

    'description': """
        Addon Custom for module Accounting & Invoicing
    """,

    'author': "Yohanes Ho",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Customize Module',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 
        'account',
        'sale'
    ],

    # always loaded
    'data': [
        'views/res_config_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}