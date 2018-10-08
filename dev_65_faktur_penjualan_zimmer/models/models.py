# -*- coding: utf-8 -*-

from odoo import models, fields, api
import amount_in_text_custom

class AccountInvoice(models.Model):
	_name = 'account.invoice'
	_inherit = 'account.invoice'

	@api.multi
	def invoice_print(self):
		""" Print the invoice and mark it as sent, so that we can see more
			easily the next step of the workflow
		"""
		self.ensure_one()
		self.sent = True
		return self.env['report'].get_action(self, 'dev_65_faktur_penjualan_zimmer.report_invoice')

	def amount_to_text(self, amount, currency):
		terbilang = amount_in_text_custom.terbilang(amount,'Rupiah','id') 
		return terbilang

	def get_address_from_so(self):
		querry = "SELECT so.customer_address FROM account_invoice ai INNER JOIN sale_order so ON so.name = ai.origin WHERE ai.origin IS NOT NULL AND ai.origin = %s;"
		param = [self.origin]

		self._cr.execute(querry,param)
		_hasil = self._cr.dictfetchall()
		return _hasil

	def get_dp_from_so(self):
		querry = "SELECT so.downpayment FROM account_invoice ai INNER JOIN sale_order so ON so.name = ai.origin WHERE ai.origin IS NOT NULL AND ai.origin = %s;"
		param = [self.origin]

		self._cr.execute(querry,param)
		_hasil = self._cr.dictfetchall()
		return _hasil

class SaleOrder(models.Model):
	_inherit = "sale.order"

	@api.multi
	def print_quotation(self):
		self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
		return self.env['report'].get_action(self, 'dev_65_faktur_penjualan_zimmer.report_order_zimmer')