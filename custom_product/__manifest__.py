# -*- coding: utf-8 -*-
{
    'name': "Custom Product",

    'summary': """
        Customization Module Product Variant""",

    'description': """
This customization implements on module
=======================================

Product

    """,

    'author': "Yohanes Ho",
    'website': "",
    'category': 'Customize Module',
    'version': '0.1',
    "sequence": 1,
    'depends': [
        'base', 
        'product',
    ],

    'data': [
        'views/product_attribute.xml',
    ],
}