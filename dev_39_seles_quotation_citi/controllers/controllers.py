# -*- coding: utf-8 -*-
from odoo import http

# class Dev39SelesQuotationCiti(http.Controller):
#     @http.route('/dev_39_seles_quotation_citi/dev_39_seles_quotation_citi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dev_39_seles_quotation_citi/dev_39_seles_quotation_citi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dev_39_seles_quotation_citi.listing', {
#             'root': '/dev_39_seles_quotation_citi/dev_39_seles_quotation_citi',
#             'objects': http.request.env['dev_39_seles_quotation_citi.dev_39_seles_quotation_citi'].search([]),
#         })

#     @http.route('/dev_39_seles_quotation_citi/dev_39_seles_quotation_citi/objects/<model("dev_39_seles_quotation_citi.dev_39_seles_quotation_citi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dev_39_seles_quotation_citi.object', {
#             'object': obj
#         })