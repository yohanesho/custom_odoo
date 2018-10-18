from odoo import api, fields, models, _
import amount_in_text_custom

class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    def amount_to_text(self, amount, currency):
        convert_amount_in_words = amount_in_text_custom.terbilang(amount, 'Rupiah', 'id')
        return convert_amount_in_words