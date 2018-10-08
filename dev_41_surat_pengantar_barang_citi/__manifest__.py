# -*- coding: utf-8 -*-
{
    'name': "dev_41_surat_pengantar_barang_citi",

    'summary': """
        Report Surat Pengantar Barang Untuk PT. Citi Interiorindo""",

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
    'depends': ['base','report','sale','sale_oplos'],

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