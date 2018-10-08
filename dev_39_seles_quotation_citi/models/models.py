# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class dev_39_seles_quotation_citi(models.Model):
#     _name = 'dev_39_seles_quotation_citi.dev_39_seles_quotation_citi'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
# -*- coding: utf-8 -*-

from datetime import datetime
import time
from odoo import api, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ReportDev39SelesQuotationCitiQuotation(models.AbstractModel):
	_name = 'report.dev_39_seles_quotation_citi.report_quotation'
	
	def _sum_discount(self, price, sp_detail):
		result = 0
		# print 'price. . .. ',price,sp_detail
		if (price * sp_detail.product_uom_qty):
			result = ( sp_detail.discount / (price * sp_detail.product_uom_qty)) * 100
		return result

	@api.model
	def render_html(self, docids, data=None):
		data['computed'] = {}
		context = dict(self.env.context or {})
		model = self.env.context.get('active_model')
		if context and context.get('active_ids'):
			# Browse the selected objects via their reference in context
			model = context.get('active_model') or context.get('model')
			# with_context(context).
		docs = self.env['sale.order'].browse(docids)
		obj_partner = self.env['res.partner']
		docargs = {
			'doc_ids': docids,
			'doc_model': self.env['sale.order'],
			'time': time,
			'data':data,
			'docs':docs,
			'sum_discount': self._sum_discount,
		}
		return self.env['report'].render('dev_39_seles_quotation_citi.report_quotation', docargs)
