# -*- coding: utf-8 -*-
from odoo import http

# class ReportFaktur(http.Controller):
#     @http.route('/report_faktur/report_faktur/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_faktur/report_faktur/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_faktur.listing', {
#             'root': '/report_faktur/report_faktur',
#             'objects': http.request.env['report_faktur.report_faktur'].search([]),
#         })

#     @http.route('/report_faktur/report_faktur/objects/<model("report_faktur.report_faktur"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_faktur.object', {
#             'object': obj
#         })