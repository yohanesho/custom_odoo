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
    "sequence": 1,
    # any module necessary for this one to work correctly
    'depends': [
        'base', 
        'account',
        'sale',
        'stock',
        'purchase',
    ],

    # always loaded
    'data': [
        'views/res_config_view.xml',
        'views/stock_picking_validator.xml',
        'views/sale_order_view.xml',
        'views/sale_history_view.xml',
        'wizard/account_report_product_ledger_view.xml',
        'data/ir_cron.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}