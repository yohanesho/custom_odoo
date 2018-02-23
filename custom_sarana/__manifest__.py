# -*- coding: utf-8 -*-
{
    'name': "Custom Addon",

    'summary': """
        Customization Module for PT. Sarana""",

    'description': """
This customization implements on module
=======================================

Accounting & Finance

Purchase Management

CRM

Sales Management

Inventory Management

Manufacturing
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
        'sale',
        'stock',
    ],

    # always loaded
    'data': [
        'views/res_config_view.xml',
        'views/stock_picking_validator.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}