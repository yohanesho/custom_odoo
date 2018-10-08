# -*- coding: utf-8 -*-
from odoo import http

# class Dev48SoAdditionalField(http.Controller):
#     @http.route('/dev_48_so_additional_field/dev_48_so_additional_field/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dev_48_so_additional_field/dev_48_so_additional_field/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dev_48_so_additional_field.listing', {
#             'root': '/dev_48_so_additional_field/dev_48_so_additional_field',
#             'objects': http.request.env['dev_48_so_additional_field.dev_48_so_additional_field'].search([]),
#         })

#     @http.route('/dev_48_so_additional_field/dev_48_so_additional_field/objects/<model("dev_48_so_additional_field.dev_48_so_additional_field"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dev_48_so_additional_field.object', {
#             'object': obj
#         })