# -*- coding: utf-8 -*-
{
    'name': "dev_64_Proforma_invoice_zimmer",

    'summary': """
        Report Proforma Invoice Untuk PT. ZIMMER
        """,

    'description': """
        1. Qweb report proforma invoice
    """,

    'author': "Integral Indonesia",
    'website': "http://www.integralindo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report','sale','dev_57_so_customer_address'],

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