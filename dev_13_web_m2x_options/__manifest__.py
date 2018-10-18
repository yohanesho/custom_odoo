# -*- coding: utf-8 -*-

{
    "name": 'dev_13_web_m2x_options',
    "version": "10.0.1.1.0",
    "depends": [
        'base',
        'web',
    ],
    'qweb': [
        'static/src/xml/base.xml',
    ],
    'license': 'AGPL-3',
    'data': [
        'views/view.xml',
       'parameter/ir.config_parameter.csv', #setup parameter lewat csv
        #'parameter/param_for_hide_and_show_button.xml' # setup parameter lewat xml
    ],
    "author": "ACSONE SA/NV, 0k.io, Tecnativa, "
              "Odoo Community Association (OCA)",
    'installable': True,
}
