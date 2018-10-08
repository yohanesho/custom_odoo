# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomerModel(models.Model):
	_inherit = 'res.partner'

	shipped_address = fields.Char(string="Shipped Address")
	