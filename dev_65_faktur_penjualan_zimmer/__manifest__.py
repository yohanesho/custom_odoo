# -*- coding: utf-8 -*-
{
    'name': "dev_65_Faktur_Penjualan_zimmer",

    'summary': """
        Report Faktur Penjualan Untuk PT. ZIMMER
        """,

    'description': """
        1. Qweb report faktur penjualan
    """,

    'author': "Integral Indonesia",
    'website': "http://www.integralindo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report','account','sale','dev_57_so_customer_address','dev_48_so_additional_field'],

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