# -*- coding: utf-8 -*-
from odoo import http

# class ReportTrialBalanceCustom(http.Controller):
#     @http.route('/report_trial_balance_custom/report_trial_balance_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_trial_balance_custom/report_trial_balance_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_trial_balance_custom.listing', {
#             'root': '/report_trial_balance_custom/report_trial_balance_custom',
#             'objects': http.request.env['report_trial_balance_custom.report_trial_balance_custom'].search([]),
#         })

#     @http.route('/report_trial_balance_custom/report_trial_balance_custom/objects/<model("report_trial_balance_custom.report_trial_balance_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_trial_balance_custom.object', {
#             'object': obj
#         })