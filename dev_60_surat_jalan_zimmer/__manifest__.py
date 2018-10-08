# -*- coding: utf-8 -*-
{
    'name': "dev_60_surat_jalan_zimmer",

    'summary': """
        Report Surat Pengantar Barang untuk PT. ZIMMER RATTAN
        """,

    'description': """
        1. Qweb report SPB
    """,

    'author': "Integral Indonesia",
    'website': "http://www.integralindo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report','sale','dev_57_so_customer_address','dev_48_so_additional_field'],

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