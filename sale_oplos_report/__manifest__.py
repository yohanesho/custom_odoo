# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Oplos Report',
    'version': '1.0',
    'author': 'Davidsetiyadi@gmail.com',
    'category': 'Custom Development',
    'summary': 'Sale Orders Report',
    'description': """
    Sales Oplos
""",
    'website': '',
    'depends': ['sale','sale_stock','stock','sale_stock','vit_efaktur','sale_oplos'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/oplos_report.xml',
        'report/oplos_report.xml',
        'report/report_invoice.xml',
        'report/proforma_invoice.xml',
        # 'views/account_views.xml',
        # 'views/stock_views.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}