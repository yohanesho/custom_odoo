# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class dev_41_surat_pengantar_barang_citi(models.Model):
#     _name = 'dev_41_surat_pengantar_barang_citi.dev_41_surat_pengantar_barang_citi'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Picking(models.Model):
	_inherit = "stock.picking"

	# TDE FIXME: separate those two kind of pack operations

	@api.multi
	def do_print_picking(self):
		self.write({'printed': True})
		# print 'action_confirmss-sad------------',self.sale_id.name
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
		return self.env["report"].get_action(self, 'dev_41_surat_pengantar_barang_citi.report_surat_pengantar')