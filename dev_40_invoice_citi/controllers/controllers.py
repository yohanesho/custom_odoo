# -*- coding: utf-8 -*-
from odoo import http

# class Dev40InvoiceCiti(http.Controller):
#     @http.route('/dev_40_invoice_citi/dev_40_invoice_citi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dev_40_invoice_citi/dev_40_invoice_citi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dev_40_invoice_citi.listing', {
#             'root': '/dev_40_invoice_citi/dev_40_invoice_citi',
#             'objects': http.request.env['dev_40_invoice_citi.dev_40_invoice_citi'].search([]),
#         })

#     @http.route('/dev_40_invoice_citi/dev_40_invoice_citi/objects/<model("dev_40_invoice_citi.dev_40_invoice_citi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dev_40_invoice_citi.object', {
#             'object': obj
#         })