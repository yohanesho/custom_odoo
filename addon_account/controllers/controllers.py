# -*- coding: utf-8 -*-
from odoo import http

# class AddonAccount(http.Controller):
#     @http.route('/addon_account/addon_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/addon_account/addon_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('addon_account.listing', {
#             'root': '/addon_account/addon_account',
#             'objects': http.request.env['addon_account.addon_account'].search([]),
#         })

#     @http.route('/addon_account/addon_account/objects/<model("addon_account.addon_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('addon_account.object', {
#             'object': obj
#         })