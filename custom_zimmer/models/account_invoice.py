from odoo import models, fields, api

class account_invoice(models.Model):
    _inherit = ['account.invoice']

    order_ids = fields.Many2many('sale.order', compute='_compute_order_ids', string='Order associated to this invoice')
    invoice_number = fields.Char(string="Number", readonly=False, states={'paid': [('readonly', True)],}, copy=False,)

    @api.multi
    @api.depends('invoice_line_ids.sale_line_ids')
    def _compute_order_ids(self):
        for inv in self:
            if len(inv.invoice_line_ids) > 0 and inv.mapped('invoice_line_ids').mapped('sale_line_ids'):
                order_lines = inv.mapped('invoice_line_ids').mapped('sale_line_ids')
                print 'order_lines: ', order_lines
                inv.order_ids = self.env['sale.order'].search([('id', '=', order_lines[0].order_id.id)]) if order_lines else []