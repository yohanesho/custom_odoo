# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Varian Optional',
    'version': '1.3',
    'author': 'Davidsetiyadi@gmail.com',
    'category': 'Custom Development',
    'summary': 'Sale Orders Custom',
    'description': """
    Sales Custom
""",
    'website': '',
    'depends': ['base','sale','stock','account','sale_stock','dev_48_so_additional_field'],
    'data': [
        'views/product_atributtes.xml',
        'views/product_template_views.xml',
        'views/sale_view.xml',
        'views/account_view.xml',
        'views/sale_report_template.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
