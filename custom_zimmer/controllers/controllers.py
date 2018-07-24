# -*- coding: utf-8 -*-
from odoo import http

# class CustomZimer(http.Controller):
#     @http.route('/custom_zimer/custom_zimer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_zimer/custom_zimer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_zimer.listing', {
#             'root': '/custom_zimer/custom_zimer',
#             'objects': http.request.env['custom_zimer.custom_zimer'].search([]),
#         })

#     @http.route('/custom_zimer/custom_zimer/objects/<model("custom_zimer.custom_zimer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_zimer.object', {
#             'object': obj
#         })