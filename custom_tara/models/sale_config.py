from odoo import models, fields, api

class SaleConfiguration(models.TransientModel):
    _inherit = 'sale.config.settings'

    group_show_price = fields.Boolean("Show price",implied_group='custom_tara.group_show_price',)

    @api.onchange('group_show_price')
    def _onchange_group_show_price(self):
        self.update({
            'sale_show_tax': 'subtotal',
            'group_show_price_total': self.group_show_price,
            'group_show_price_subtotal': self.group_show_price,
            'group_discount_per_so_line': 0 if not self.group_show_price else self.group_discount_per_so_line,
            'sale_pricelist_setting': 'fixed' if not self.group_show_price else self.sale_pricelist_setting,
        })