# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'
	colour_att_value_id = fields.Many2one('product.attribute.value', string='Colour')
	other_att_value_id = fields.Many2one('product.attribute.value', string='Other')
	product_varian_tmpl_id = fields.Many2one('product.template', ondelete='restrict', string='Products', required=True)
	qty_varian = fields.Float(
		compute='_get_varian_qty', string='Qty Available', store=False, readonly=True,
		digits=dp.get_precision('Product Unit of Measure'))
	is_colour = fields.Boolean('Colour')
	is_other = fields.Boolean('Other')

	@api.depends('product_id')
	def _get_varian_qty(self):
		"""
		Compute the quantity to invoice. If the invoice policy is order, the quantity to invoice is
		calculated from the ordered quantity. Otherwise, the quantity delivered is used.
		"""
		for line in self:
			if line.product_id:
				line.qty_varian = line.product_id.qty_available
			else:
				line.qty_varian = 0

	@api.multi
	@api.onchange('product_id')
	def product_id_change(self):
		if not self.product_id:
			return {'domain': {'product_uom': []}}
		colour_att_value_ids = []
		other_att_value_ids = []
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
					
		# for attribute in product.product_tmpl_id.attribute_line_ids:
		# 	print 'attribute. . ',attribute.type_variant
		# 	if attribute.type_variant == 'colours':
		# 		for value in attribute.value_ids:
		# 			for varian in product.product_variant_ids:
		# 				if varian.qty_available > 0:
		# 					value_ids = [x.id for x in varian.attribute_value_ids]
		# 					if value.id in value_ids:
		# 						colour_att_value_ids.append(value.id)

		# 	if attribute.type_variant == 'other':
		# 		for value in attribute.value_ids:
		# 			for varian in product.product_variant_ids:
		# 				if varian.qty_available > 0:
		# 					value_ids = [x.id for x in varian.attribute_value_ids]
		# 					if value.id in value_ids:
		# 						other_att_value_ids.append(value.id)
		# if colour_att_value_ids:
		# 	domain['colour_att_value_id'] = [('id','=',colour_att_value_ids)]
		# if other_att_value_ids:
		# 	domain['other_att_value_id'] = [('id','=',other_att_value_ids)]
		# if not colour_att_value_ids:
		# 	domain['colour_att_value_id'] = [('id','=',False)]
		# if not other_att_value_ids:
		# 	domain['other_att_value_id'] = [('id','=',False)]

		name = product.name_get()[0][1]
		if product.description_sale:
			name += '\n' + product.description_sale
		vals['name'] = name
		
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
	@api.onchange('product_varian_tmpl_id')
	def tmpl_id_change(self):
		if not self.product_varian_tmpl_id:
			return False
		vals = {}	
		domain = {}	
		colour_att_value_ids = []
		other_att_value_ids = []
		if self.product_varian_tmpl_id.product_variant_ids:
			vals['product_id'] = self.product_varian_tmpl_id.product_variant_ids[0].id
		
		vals['colour_att_value_id'] = False
		vals['other_att_value_id'] = False
		vals['is_colour'] = False
		vals['is_other'] = False
		for attribute in self.product_varian_tmpl_id.attribute_line_ids:
			if attribute.type_variant == 'colours':
				vals['is_colour'] = True
				colour_att_value_ids = [x.id for x in attribute.value_ids]
			

			if attribute.type_variant == 'other':
				vals['is_other'] = True
				other_att_value_ids = [x.id for x in attribute.value_ids]
				

		# for products in self.product_varian_tmpl_id.product_variant_ids:
		# 	if products.qty_available > 0:
		# 		for values in products.attribute_value_ids:
		# 			if values.attribute_id.type_variant == 'colours':
		# 				colour_att_value_ids.append(values.id)
		# 			if values.attribute_id.type_variant == 'other':
		# 				other_att_value_ids.append(values.id)

		if colour_att_value_ids:								
			domain['colour_att_value_id'] = [('id','=',colour_att_value_ids)]
		if not colour_att_value_ids:
			domain['colour_att_value_id'] = [('id','=',False)]
		if other_att_value_ids:
			domain['other_att_value_id'] = [('id','=',other_att_value_ids)]
		if not other_att_value_ids:
			domain['other_att_value_id'] = [('id','=',False)]
		self.update(vals)
		return {'domain': domain}

	@api.multi
	@api.onchange('colour_att_value_id','other_att_value_id')
	def att_id_change(self):
		if not self.product_id:
			return False

		vals = {}
		name = ''
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
		print 'teststst'
		if self.colour_att_value_id:
			# vals['name'] = name + ' ('+self.colour_att_value_id.name+ ')'
			for varian in self.product_varian_tmpl_id.product_variant_ids:
				if self.colour_att_value_id in varian.attribute_value_ids:
					vals['product_id'] = varian.id

		elif self.other_att_value_id:
			# vals['name'] = name + ' ('+self.other_att_value_id.name+ ')'
			for varian in self.product_varian_tmpl_id.product_variant_ids:
				if self.other_att_value_id in varian.attribute_value_ids:
					vals['product_id'] = varian.id
		if self.colour_att_value_id and self.other_att_value_id:
			for varian in self.product_varian_tmpl_id.product_variant_ids:
				varian_data = []
				# print 'varian . . .. ',varian
				varian_data = [ attribute.id for attribute in varian.attribute_value_ids]
				# print 'varian_data. . . .',varian_data
				varian_1 = [self.colour_att_value_id.id,self.other_att_value_id.id]
				varian_2 = [self.other_att_value_id.id, self.colour_att_value_id.id]
				print 'varian . . .. ',varian_1,varian_2,'varian_data',varian_data
				if varian_1 == varian_data:					
					print 'varian 1'
					vals['product_id'] = varian.id
				elif varian_2 == varian_data:					
					print 'varian_2'
					vals['product_id'] = varian.id

				# for varian in product
			# vals['product_id'] = 
			# vals['name'] = name + ' ('+ self.other_att_value_id.name+', ' + self.colour_att_value_id.name +')'
		
		self.update(vals)

	@api.multi
	def _prepare_invoice_line(self, qty):
		"""
		Prepare the dict of values to create the new invoice line for a sales order line.

		:param qty: float quantity to invoice
		"""
		res = super(SaleOrderLine, self)._prepare_invoice_line(qty)       
		print 'suksessss',res
		res['colour_att_value_id'] = self.colour_att_value_id.id
		res['other_att_value_id'] = self.other_att_value_id.id
		res['product_varian_tmpl_id'] = self.product_varian_tmpl_id.id
		res['is_colour'] = self.is_colour
		res['is_other'] = self.is_other
		
		return res


	@api.onchange('product_uom_qty', 'product_uom', 'route_id')
	def _onchange_product_id_check_availability(self):
		print 'testst .. . . .. '
		if not self.product_id or not self.product_uom_qty or not self.product_uom:
			self.product_packaging = False
			return {}
		if self.product_id.type == 'product':
			precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
			product_qty = self.product_uom._compute_quantity(self.product_uom_qty, self.product_id.uom_id)
			if float_compare(self.product_id.virtual_available, product_qty, precision_digits=precision) == -1:
				is_available = self._check_routing()
				if not is_available:
					print 'not use again'
					# warning_mess = {
					#     'title': _('Not enough inventory!'),
					#     'message' : _('You plan to sell %s %s but you only have %s %s available!\nThe stock on hand is %s %s.') % \
					#         (self.product_uom_qty, self.product_uom.name, self.product_id.virtual_available, self.product_id.uom_id.name, self.product_id.qty_available, self.product_id.uom_id.name)
					# }
					# return {'warning': warning_mess}
		return {}
