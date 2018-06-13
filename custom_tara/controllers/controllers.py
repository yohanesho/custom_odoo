# -*- coding: utf-8 -*-
from odoo import http

# class CustomTara(http.Controller):
#     @http.route('/custom_tara/custom_tara/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_tara/custom_tara/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_tara.listing', {
#             'root': '/custom_tara/custom_tara',
#             'objects': http.request.env['custom_tara.custom_tara'].search([]),
#         })

#     @http.route('/custom_tara/custom_tara/objects/<model("custom_tara.custom_tara"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_tara.object', {
#             'object': obj
#         })