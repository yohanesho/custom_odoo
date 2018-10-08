# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Oplos',
    'version': '1.0',
    'author': 'Davidsetiyadi@gmail.com',
    'category': 'Custom Development',
    'summary': 'Sale Orders Custom',
    'description': """
    Sales Oplos
""",
    'website': '',
    'depends': ['base','sale','sale_stock','delivery','stock','stock_account','vit_efaktur','product_bundle_pack'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/sale_views.xml',
        'views/account_views.xml',
        'views/stock_views.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}