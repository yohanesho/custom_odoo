# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
import itertools
import psycopg2

import odoo.addons.decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError,ValidationError, except_orm
from odoo.osv import expression

class ProductTemplate(models.Model):
	_inherit = "product.template"

	ace_code = fields.Char('ACE Code', index=True)
	sale_oplos_ids = fields.Many2many('product.template', 'product_template_oplos_rel','template_1_id','template_2_id', string='Oplos Code', copy=False)

	@api.multi
	def name_get(self):
		if self._context.get('default_internal_reference'):
			print '_context .. . . ..'
			return [(template.id, '%s' % (template.default_code ))
				for template in self]

		return [(template.id, '%s%s' % (template.default_code and '[%s] ' % template.default_code or '', template.name))
				for template in self]
				
class ProductProduct(models.Model):
	_inherit = "product.product"

	@api.model
	def name_search(self, name='', args=None, operator='ilike', limit=100):
		if not args:
			args = []
		if name:
			# print 'david. . . ........................'
			positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
			products = self.env['product.product']
			if operator in positive_operators:
				products = self.search([('default_code', '=', name)] + args, limit=limit)
				if not products:
					products = self.search([('barcode', '=', name)] + args, limit=limit)
					if not products:
						products = self.search([('ace_code', '=', name)] + args, limit=limit)
			
			if not products and operator not in expression.NEGATIVE_TERM_OPERATORS:
				# Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
				# on a database with thousands of matching products, due to the huge merge+unique needed for the
				# OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
				# Performing a quick memory merge of ids in Python will give much better performance
				products = self.search(args + [('default_code', operator, name)], limit=limit)
				if not limit or len(products) < limit:
					# we may underrun the limit because of dupes in the results, that's fine
					limit2 = (limit - len(products)) if limit else False
					products += self.search(args + [('name', operator, name), ('id', 'not in', products.ids)], limit=limit2)
			elif not products and operator in expression.NEGATIVE_TERM_OPERATORS:
				products = self.search(args + ['&', ('default_code', operator, name), ('name', operator, name)], limit=limit)
			if not products and operator in positive_operators:
				ptrn = re.compile('(\[(.*?)\])')
				res = ptrn.search(name)
				if res:
					products = self.search([('default_code', '=', res.group(2))] + args, limit=limit)
			# still no results, partner in context: search on supplier info as last hope to find something
			if not products and self._context.get('partner_id'):
				suppliers = self.env['product.supplierinfo'].search([
					('name', '=', self._context.get('partner_id')),
					'|',
					('product_code', operator, name),
					('product_name', operator, name)])
				if suppliers:
					products = self.search([('product_tmpl_id.seller_ids', 'in', suppliers.ids)], limit=limit)
		else:
			products = self.search(args, limit=limit)
		return products.name_get()

# class CustomSaleOplos(models.Model):
# 	_name = "custom.sale.oplos"
	
# 	name = fields.Many2one('product.template', string='Oplos Code')	
# 	ace_code = fields.Char('Ace Code', compute='_compute_default_ace_code', store=True)
# 	oplos_description = fields.Char('Dec Code', compute='_compute_default_ace_code', store=True)

# 	@api.depends('name', 'name.ace_code')
# 	def _compute_default_ace_code(self):
# 		for sale_oplos in self:
# 			sale_oplos.ace_code = sale_oplos.name.ace_code
# 			sale_oplos.oplos_description = sale_oplos.name.name


	# @api.depends('name', 'name.name')
	# def _compute_default_oplos_description
	# 	for sale_oplos in self:
	# 		sale_oplos.oplos_description = sale_oplos.name.name
