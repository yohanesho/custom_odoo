# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp

class ProcurementOrder(models.Model):
	""" Procurement Orders """
	_inherit = "procurement.order"
	oplos_template_id = fields.Many2one('product.template', string='Oplos', change_default=True)

	def _get_stock_move_values(self):
		vals = super(ProcurementOrder, self)._get_stock_move_values()
		vals.update({
			'oplos_template_id': self.oplos_template_id.id,
		})
		return vals

class SaleOrder(models.Model):
	_inherit = "sale.order"

	@api.multi
	def print_surat_jalan(self):
		'''
		This function returns an action that display existing delivery orders
		of given sales order ids. It can either be a in a list or in a form
		view, if there is only one delivery order to show.
		'''
		action = self.env.ref('stock.action_picking_tree_all').read()[0]

		pickings = self.mapped('picking_ids')
		# if len(pickings) > 1:
			# action['domain'] = [('id', 'in', pickings.ids)]
		for picking_id in pickings.ids:
			picking = self.env['stock.picking'].browse(picking_id)
			# print 'pickings. . . . ',picking
			return picking.do_print_picking()
		# elif pickings:
			# action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
			# action['res_id'] = pickings.id
			# print 'pickings',pickings
			# self.env['stock.picking'].do_print_picking(pickings)
			# pickings.do_print_picking()

		return True

	@api.multi
	def print_invoice(self):
		for order in self:
			invoice_ids = order.order_line.mapped('invoice_lines').mapped('invoice_id')
			for invoice in invoice_ids:
				# print invoice,'invoiceeee'
				return self.env["report"].get_action(invoice, 'account.report_invoice')

	@api.multi
	def print_proforma(self):
		for order in self:
			# invoice_ids = order.order_line.mapped('invoice_lines').mapped('invoice_id')
			# for invoice in invoice_ids:
			return self.env["report"].get_action(self, 'sale_oplos_report.report_proforma')

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	@api.model
	def create(self, values):
		onchange_fields = ['name', 'price_unit', 'product_uom', 'tax_id']
		if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
			line = self.new(values)
			# line.product_id_change()
			line.oplos_id_change()
			for field in onchange_fields:
				if field not in values:
					values[field] = line._fields[field].convert_to_write(line[field], line)
		line = super(SaleOrderLine, self).create(values)
		if line.state == 'sale':
			line._action_procurement_create()

		return line

	oplos_template_id = fields.Many2one('product.template', string='Oplos', change_default=True, ondelete='restrict')

	@api.multi
	@api.onchange('product_id')
	def product_id_change(self):
		if not self.product_id:
			return {'domain': {'product_uom': []}}
		colour_att_value_ids = []
		oplos_template_ids = []
		vals = {}
		domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
		if not self.product_uom or (self.product_id.uom_id.category_id.id != self.product_uom.category_id.id):
			vals['product_uom'] = self.product_id.uom_id

		product = self.product_id.with_context(
			lang=self.order_id.partner_id.lang,
			partner=self.order_id.partner_id.id,
			quantity=self.product_uom_qty,
			date=self.order_id.date_order,
			pricelist=self.order_id.pricelist_id.id,
			uom=self.product_uom.id
		)
		# if self.product_id.type == 'product':
			# precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
			# product_qty = self.product_uom._compute_quantity(self.product_uom_qty, self.product_id.uom_id)
			# if float_compare(self.product_id.virtual_available, product_qty, precision_digits=precision) == -1:
			# 	is_available = self._check_routing()
			# 	if not is_available:
			# 		warning_mess = {
			# 			'title': _('Not enough inventory!'),
			# 			'message' : _('You plan to sell %s %s but you only have %s %s available!\nThe stock on hand is %s %s.') % \
			# 				(self.product_uom_qty, self.product_uom.name, self.product_id.virtual_available, self.product_id.uom_id.name, self.product_id.qty_available, self.product_id.uom_id.name)
			# 		}
			# 		return {'warning': warning_mess}
					
		for oplos in product.product_tmpl_id.sale_oplos_ids:	
			oplos_template_ids.append(oplos.id)
		
		if oplos_template_ids:
			domain['oplos_template_id'] = [('id','=',oplos_template_ids)]
		else:
			domain['oplos_template_id'] = [('id','=',False)]
		name = product.name_get()[0][1]
		if product.description_sale:
			name += '\n' + product.description_sale
		vals['name'] = name
		vals['oplos_template_id'] = False
		self._compute_tax_id()

		if self.order_id.pricelist_id and self.order_id.partner_id:
			vals['price_unit'] = self.env['account.tax']._fix_tax_included_price(self._get_display_price(product), product.taxes_id, self.tax_id)
		self.update(vals)

		title = False
		message = False
		warning = {}
		if product.sale_line_warn != 'no-message':
			title = _("Warning for %s") % product.name
			message = product.sale_line_warn_msg
			warning['title'] = title
			warning['message'] = message
			if product.sale_line_warn == 'block':
				self.product_id = False
			return {'warning': warning}
		return {'domain': domain}

	@api.multi
	@api.onchange('oplos_template_id')
	def oplos_id_change(self):
		if not self.product_id:
			return False
		vals = {}
		name = ''
		domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
		if not self.product_uom or (self.product_id.uom_id.category_id.id != self.product_uom.category_id.id):
			vals['product_uom'] = self.product_id.uom_id

		product = self.product_id.with_context(
			lang=self.order_id.partner_id.lang,
			partner=self.order_id.partner_id.id,
			quantity=self.product_uom_qty,
			date=self.order_id.date_order,
			pricelist=self.order_id.pricelist_id.id,
			uom=self.product_uom.id
		)
		name = product.name_get()[0][1]
		vals['name'] = name
		if self.oplos_template_id:
			vals['name'] = self.oplos_template_id.name_get()[0][1]
		if self.order_id.pricelist_id and self.order_id.partner_id:			
			vals['price_unit'] = self.env['account.tax']._fix_tax_included_price(self._get_display_price(product), product.taxes_id, self.tax_id)

		
		self.update(vals)

	@api.multi
	def _prepare_invoice_line(self, qty):
		"""
		Prepare the dict of values to create the new invoice line for a sales order line.

		:param qty: float quantity to invoice
		"""
		res = super(SaleOrderLine, self)._prepare_invoice_line(qty)       
		res['oplos_template_id'] = self.oplos_template_id.id
		
		return res

	@api.multi
	def _prepare_order_line_procurement(self, group_id=False):
		vals = super(SaleOrderLine, self)._prepare_order_line_procurement(group_id=group_id)
		# print 'vals. . .',vals
		# vals.append({
		# 	'oplos_template_id': self.oplos_template_id.id,
		# })
		vals[0]['oplos_template_id'] = self.oplos_template_id.id
		return vals

	