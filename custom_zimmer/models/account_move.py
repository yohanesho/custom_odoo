from odoo import models, fields, api

class account_move(models.Model):
    _inherit = ['account.move']

    invoice_id = fields.Many2one('account.invoice', compute='_compute_invoice_id', string='Invoice associated to this account move.')
    invoice_number = fields.Char(string=u'Proforma Number', related='invoice_id.invoice_number',)
    
    @api.one
    def _compute_invoice_id(self):
        invoice = self.env['account.invoice'].search([('move_id', '=', self.id)])
        if invoice:
            self.invoice_id = invoice.id