from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountReportProductLedger(models.TransientModel):
    _name = 'account.report.product.ledger'
    _inherit = ['account.common.account.report']
    _description = "Product Ledger Report"

    initial_balance = fields.Boolean(
        string='Include Initial Balances',
        help='If you selected date, this field allow you to add a row to display the amount of debit/credit/balance that precedes the filter you\'ve set.')
    sortby = fields.Selection(
        [('sort_date', 'Date'), ('sort_category_product', 'Product Category & Product')], 
        string='Sort by', 
        required=True, 
        default='sort_date')

    product_categ_ids = fields.Many2many('product.category', string='Product Categories', required=True, default=lambda self: self.env['product.category'].search([]))

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update(self.read(['initial_balance', 'sortby','product_categ_ids'])[0])
        if data['form'].get('initial_balance') and not data['form'].get('date_from'):
            raise UserError(_("You must define a Start Date"))
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env['report'].with_context(landscape=True).get_action(records, 'custom_sarana.report_productledger', data=data)