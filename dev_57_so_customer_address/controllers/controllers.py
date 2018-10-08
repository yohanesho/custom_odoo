# -*- coding: utf-8 -*-
from odoo import http

# class Dev57SoCustomerAddress(http.Controller):
#     @http.route('/dev_57_so_customer_address/dev_57_so_customer_address/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dev_57_so_customer_address/dev_57_so_customer_address/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dev_57_so_customer_address.listing', {
#             'root': '/dev_57_so_customer_address/dev_57_so_customer_address',
#             'objects': http.request.env['dev_57_so_customer_address.dev_57_so_customer_address'].search([]),
#         })

#     @http.route('/dev_57_so_customer_address/dev_57_so_customer_address/objects/<model("dev_57_so_customer_address.dev_57_so_customer_address"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dev_57_so_customer_address.object', {
#             'object': obj
#         })