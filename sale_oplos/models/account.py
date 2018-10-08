# -*- coding: utf-8 -*-

import json
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang

from odoo.exceptions import UserError, RedirectWarning, ValidationError

import odoo.addons.decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
	_inherit = "account.invoice.line"

	oplos_template_id = fields.Many2one('product.template', string='Oplos', change_default=True)

	@api.onchange('product_id')
	def _onchange_product_id(self):
		domain = {}
		oplos_template_ids = []
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
			
			for oplos in product.product_tmpl_id.sale_oplos_ids:	
				oplos_template_ids.append(oplos.id)

			domain['uom_id'] = [('category_id', '=', product.uom_id.category_id.id)]
			if oplos_template_ids:
				domain['oplos_template_id'] = [('id','=',oplos_template_ids)]
			else:
				domain['oplos_template_id'] = [('id','=',False)]
			if company and currency:
				if company.currency_id != currency:
					self.price_unit = self.price_unit * currency.with_context(dict(self._context or {}, date=self.invoice_id.date_invoice)).rate

				if self.uom_id and self.uom_id.id != product.uom_id.id:
					self.price_unit = product.uom_id._compute_price(self.price_unit, self.uom_id)
		return {'domain': domain}

	@api.multi
	@api.onchange('oplos_template_id')
	def oplos_id_change(self):
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
		if self.oplos_template_id:
			vals['name'] = self.oplos_template_id.name_get()[0][1]
		
		
		self.update(vals)