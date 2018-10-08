from odoo import models, fields, api

class res_company(models.Model):
    _inherit = ['product.template']

    for_deposit = fields.Boolean(
        string=u'For Deposit',
        compute='get_deposit'
    )

    def get_deposit(self):
        product_id = self.env['product.product'].browse(self.env['ir.values'].get_default('sale.config.settings', 'deposit_product_id_setting'))
        for record in self:
            record.for_deposit = record.name == product_id.name
    