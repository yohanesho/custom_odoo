{
    "name": "Custom Sales Order",
    "version": "10.1",
    "depends": [
        'sale',
    ],
    "author": "Joenan <joenannr@gmail.com>",
    "category": "",
    "description" : """Custom Sales Order""",
    'depends': ['base','sale','sale_discount_total'],
    'data': [
        'views/sale_view.xml',
    ],
    'demo':[     
    ],
    'test':[
    ],
    'application' : False,
    'installable' : True,
    'auto_install' : False,
}
