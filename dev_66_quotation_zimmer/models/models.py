# -*- coding: utf-8 -*-

from odoo import models, fields, api
import amount_in_text_custom

class SaleOrder(models.Model):
	_name = 'sale.order'
	_inherit = 'sale.order'

	def amount_to_text(self, amount, currency):
		terbilang = amount_in_text_custom.terbilang(amount,'Rupiah','id') 
		return terbilang