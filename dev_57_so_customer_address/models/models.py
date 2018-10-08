# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
	_inherit = 'sale.order'
	
	customer_address = fields.Text(string="Shipped To")
	internal_note = fields.Text()
	initial_number_so = fields.Char() #default=lambda self: self.set_value_coeg()
	po = fields.Char(string="PO No.")
	manual_number = fields.Char(string="Manual Number")
	rfq = fields.Char(string="RFQ")
	so = fields.Char(string="INV No.")
	attn = fields.Char(string="Attn.")
	
	@api.model
	def set_value_coeg(self):		
		# print "======================================================================================= JOKOMPOL"

		inisial_user = ""
		iu = self.env['res.users'].search([('id','=',self.env.user.id)]).initial_number_User
		
		if iu != False:
			inisial_user = iu

		str1 = self.env['ir.sequence'].next_by_code('sales.quotation')
		# print "====================================================================================JOKOLOL"
		
		str2 = 'SQ/'
		
		# print str1
		# print inisial_user
		# print str2

		if str1 != False and inisial_user != False and str2 != False:
			str3 = str2+inisial_user+str1
			return str3

	@api.onchange('partner_id')
	def onchange_customer_coeg(self):
		customer = self.partner_id
		self.customer_address = customer.shipped_address

		# address = ""

		# if customer:
		# 	if customer.street != False:
		# 		address = address + customer.street + '\n'
		# 	if customer.street2 != False:
		# 		address = address + customer.street2 + '\n'
		# 	if customer.city != False:
		# 		address = address + customer.city + " "
		# 	if customer.state_id.name != False:
		# 		address = address + customer.state_id.name + " " + customer.zip	
		# 	if customer.zip != False:
		# 		address = address + '\n' + customer.country_id.name
			
		# 	self.customer_address = address

class CustomerInvoice(models.Model):
	_inherit = 'account.invoice'
	
	customer_address = fields.Text(string="Shipped To")
	internal_note = fields.Text()
	mannumber_inv = fields.Char() #default=lambda self: self.set_value_coeg()

	@api.onchange('partner_id')
	def onchange_customer_coeg(self):
		customer = self.partner_id
		self.customer_address = customer.shipped_address

		# address = ""

		# if customer:
		# 	if customer.street != False:
		# 		address = address + customer.street + '\n'
		# 	if customer.street2 != False:
		# 		address = address + customer.street2 + '\n'
		# 	if customer.city != False:
		# 		address = address + customer.city + " "
		# 	if customer.state_id.name != False:
		# 		address = address + customer.state_id.name + " " + customer.zip	
		# 	if customer.zip != False:
		# 		address = address + '\n' + customer.country_id.name
			
		# 	self.customer_address = address

