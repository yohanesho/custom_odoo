# -*- coding: utf-8 -*-
{
    'name': "dev_57_so_customer_address",

    'summary': """
        This module used to make address of customer can be change in sale order
        """,

    'description': """
        1. Hide address information in So
        2. Create field address and get default address from customer        
    """,

    'author': "Integral Indonesia",
    'website': "http://www.integralindo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Form',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','dev_76_customer_additional_field'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}