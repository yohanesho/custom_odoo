# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
	_name = 'stock.picking'
	_inherit = 'stock.picking'

	def get_client_order_ref(self):
		querry = "select client_order_ref from sale_order where name = %s  ;"
		param = [self.origin]

		self._cr.execute(querry,param)
		_hasil = self._cr.dictfetchall()
		return _hasil

	def get_address_from_so(self):
		if self.origin:
			querry = "SELECT so.customer_address FROM stock_picking sp INNER JOIN sale_order so ON so.name = sp.origin WHERE sp.origin IS NOT NULL AND sp.origin = %s;"
		else:
			querry = "SELECT so.customer_address FROM stock_picking sp INNER JOIN sale_order so ON so.name = sp.origin WHERE sp.origin IS NOT NULL AND sp.origin = 'False';"
		param = [self.origin]

		self._cr.execute(querry,param)
		_hasil = self._cr.dictfetchall()
		return _hasil