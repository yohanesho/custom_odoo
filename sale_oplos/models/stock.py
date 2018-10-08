# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil import relativedelta
import time

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.addons.procurement.models import procurement
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_round, float_is_zero


class StockMove(models.Model):
	_inherit = "stock.move"

	oplos_template_id = fields.Many2one('product.template', string='Oplos', change_default=True)

	@api.onchange('product_id')
	def onchange_product_id(self):
		product = self.product_id.with_context(lang=self.partner_id.lang or self.env.user.lang)
		self.name = product.partner_ref
		oplos_template_ids = []
		self.product_uom = product.uom_id.id
		self.product_uom_qty = 1.0
		for oplos in product.product_tmpl_id.sale_oplos_ids:	
			oplos_template_ids.append(oplos.id)
		if oplos_template_ids:
			return {'domain': {	'product_uom': [('category_id', '=', product.uom_id.category_id.id)],
							'oplos_template_id': [('id','in',oplos_template_ids)]}}
		else:
			return {'domain': {	'product_uom': [('category_id', '=', product.uom_id.category_id.id)],
							'oplos_template_id': [('id','=',False)]}}

	@api.multi
	@api.onchange('oplos_template_id')
	def oplos_id_change(self):
		if not self.product_id:
			return False
		vals = {}
		# name = ''
		product = self.product_id.with_context(
			lang=self.picking_id.partner_id.lang,
			partner=self.picking_id.partner_id.id,
			quantity=self.product_uom_qty,
			uom=self.product_uom.id
		)
		name = product.name_get()[0][1]
		# vals['name'] = name
		if self.oplos_template_id:
			vals['name'] = self.oplos_template_id.name_get()[0][1]
		
		
		self.update(vals)

class Picking(models.Model):
	_inherit = "stock.picking"

	# TDE FIXME: separate those two kind of pack operations
	citi_stock_picking_line_ids = fields.One2many(
		'citi.stock.picking.line', 'picking_id', 'Product Sale',
		readonly=True)

	@api.multi
	def do_print_picking(self):
		self.write({'printed': True})
		if self.citi_stock_picking_line_ids:
			for product_sale in self.citi_stock_picking_line_ids:
				product_sale.unlink()
		if self.sale_id:
			line_data = []		
			line_dict = {}	
			for line in self.sale_id.order_line:
				line_dict = {
					'product_id': line.product_id.id,
					'product_uom_id': line.product_uom.id,
					'ordered_qty':line.product_uom_qty,
					'product_uom_qty': line.product_uom_qty,
					'oplos_template_id':line.oplos_template_id.id,
				}
				line_data.append( (0, 0, line_dict) )
				# self.write({'citi_stock_picking_line_ids':[(0, 0, line_dict)] })
			if line_data:
				self.write({'citi_stock_picking_line_ids': line_data })
		return self.env["report"].get_action(self, 'stock.report_picking')

class CitiStockPickingLine(models.Model):
	_name = "citi.stock.picking.line"
	_description = "Citi Stock Picking"

	
	picking_id = fields.Many2one(
		'stock.picking', 'Stock Picking',
		required=True,
		help='The stock operation where the packing has been made')
	product_id = fields.Many2one('product.product', 'Product', ondelete="cascade")
	product_uom_id = fields.Many2one('product.uom', 'Unit of Measure')
	name = fields.Char('Name')
	ordered_qty = fields.Float('Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'))
	product_uom_qty = fields.Float('Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'))
	oplos_template_id = fields.Many2one('product.template', string='Oplos', change_default=True)

class Quant(models.Model):
	_inherit = "stock.quant"

	ace_code = fields.Char( string='ACE Code', related='product_id.product_tmpl_id.ace_code',readonly=True)

class stock_summary_line(models.Model):
	_inherit 		= "vit.stock_summary_line"

	ace_code = fields.Char( string='ACE Code', related='product_id.product_tmpl_id.ace_code',readonly=True)
