# -*- coding: utf-8 -*-

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp
# _logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
	_inherit = "account.invoice.line"

	colour_att_value_id = fields.Many2one('product.attribute.value', string='Colour')
	other_att_value_id = fields.Many2one('product.attribute.value', string='Other')
	product_varian_tmpl_id = fields.Many2one('product.template', string='Products')
	is_colour = fields.Boolean('Colour')
	is_other = fields.Boolean('Other')


	@api.onchange('product_id')
	def _onchange_product_id(self):
		domain = {}
		colour_att_value_ids = []
		other_att_value_ids = []
		if not self.invoice_id:
			return

		part = self.invoice_id.partner_id
		fpos = self.invoice_id.fiscal_position_id
		company = self.invoice_id.company_id
		currency = self.invoice_id.currency_id
		type = self.invoice_id.type

		if not part:
			warning = {
					'title': _('Warning!'),
					'message': _('You must first select a partner!'),
				}
			return {'warning': warning}

		if not self.product_id:
			if type not in ('in_invoice', 'in_refund'):
				self.price_unit = 0.0
			domain['uom_id'] = []
		else:
			if part.lang:
				product = self.product_id.with_context(lang=part.lang)
			else:
				product = self.product_id

			self.name = product.partner_ref
			account = self.get_invoice_line_account(type, product, fpos, company)
			if account:
				self.account_id = account.id
			self._set_taxes()

			if type in ('in_invoice', 'in_refund'):
				if product.description_purchase:
					self.name += '\n' + product.description_purchase
			else:
				if product.description_sale:
					self.name += '\n' + product.description_sale

			if not self.uom_id or product.uom_id.category_id.id != self.uom_id.category_id.id:
				self.uom_id = product.uom_id.id
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

			domain['uom_id'] = [('category_id', '=', product.uom_id.category_id.id)]
			# domain['colour_att_value_id'] = [('id','=',colour_att_value_ids)]
			# domain['other_att_value_id'] = [('id','=',other_att_value_ids)]
			if company and currency:
				if company.currency_id != currency:
					self.price_unit = self.price_unit * currency.with_context(dict(self._context or {}, date=self.invoice_id.date_invoice)).rate

				if self.uom_id and self.uom_id.id != product.uom_id.id:
					self.price_unit = product.uom_id._compute_price(self.price_unit, self.uom_id)
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
		vals['product_id'] = self.product_varian_tmpl_id.product_variant_ids[0].id
		vals['is_colour'] = False
		vals['is_other'] = False
		vals['colour_att_value_id'] = False
		vals['other_att_value_id'] = False
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
			lang=self.invoice_id.partner_id.lang,
			partner=self.invoice_id.partner_id.id,
			uom=self.uom_id.id
		)
		name = product.name_get()[0][1]
		vals['name'] = name
		if self.colour_att_value_id:
			for varian in self.product_varian_tmpl_id.product_variant_ids:
				if self.colour_att_value_id in varian.attribute_value_ids:
					vals['product_id'] = varian.id
		# 	vals['name'] = name + ' ('+self.colour_att_value_id.name+ ')'
		elif self.other_att_value_id:
			for varian in self.product_varian_tmpl_id.product_variant_ids:
				if self.other_att_value_id in varian.attribute_value_ids:
					vals['product_id'] = varian.id
		# 	vals['name'] = name + ' ('+self.other_att_value_id.name+ ')'
		if self.colour_att_value_id and self.other_att_value_id:
		# 	vals['name'] = name + ' ('+ self.other_att_value_id.name+', ' + self.colour_att_value_id.name +')'
			for varian in self.product_varian_tmpl_id.product_variant_ids:
				if self.other_att_value_id and self.other_att_value_id in varian.attribute_value_ids:
					# print 'suksessss',self.colour_att_value_id, self.other_att_value_id
					vals['product_id'] = varian.id
		self.update(vals)