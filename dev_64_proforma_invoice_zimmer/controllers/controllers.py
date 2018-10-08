# -*- coding: utf-8 -*-
from odoo import http

# class ReportFaktur(http.Controller):
#     @http.route('/dev_24_report_faktur/dev_24_report_faktur/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dev_24_report_faktur/dev_24_report_faktur/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dev_24_report_faktur.listing', {
#             'root': '/dev_24_report_faktur/dev_24_report_faktur',
#             'objects': http.request.env['dev_24_report_faktur.dev_24_report_faktur'].search([]),
#         })

#     @http.route('/dev_24_report_faktur/dev_24_report_faktur/objects/<model("dev_24_report_faktur.dev_24_report_faktur"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dev_24_report_faktur.object', {
#             'object': obj
#         })