# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class SaleOrder(models.Model):
	# _name = 'sale.order'
	_inherit = 'sale.order'

	downpayment = fields.Integer(string="DP(%)", default=50)
	initial_number_so = fields.Char() #default=lambda self: self.set_value_coeg()
	po = fields.Char(string="PO No.")
	manual_number = fields.Char(string="Manual Number")
	rfq = fields.Char(string="RFQ")
	so = fields.Char(string="INV No.")
	attn = fields.Char(string="Attn.")
	customer_address = fields.Text(string="Shipped To")
	internal_note = fields.Text()

# class SaleOrderLine(models.Model):
	# _inherit = 'sale.order.line'

	amount_dp = fields.Monetary(string="Amount DownPayment", compute='_get_amount_dp_from_so')

	def _get_amount_dp_from_so(self):
		for coeg in self:
			querry = "SELECT (amount_total * downpayment / 100) AS amount_dp FROM sale_order WHERE id = %s;"

			param = [coeg.id]

			self._cr.execute(querry,param)
			_hasil = self._cr.dictfetchall()
			
			for data in _hasil:
				coeg.amount_dp = data['amount_dp']
		


	# date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
	# validity_date = fields.Date(string='Expiration Date', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},        help="Manually set the expiration date of your quotation (offer), or it will set the date automatically based on the template if online quotation is installed.", default=datetime.now()+timedelta(days=14))

	# @api.onchange('date_order')
	# def date_order_diubah_coy(self):
	# 	self.validity_date = self.date_order + timedelta(days=14)