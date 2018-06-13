from odoo import models, fields, api, tools
from odoo.fields import Datetime as fieldsDatetime

import odoo.addons.decimal_precision as dp

class SaleHistoryPrice(models.Model):
    _name='sale.history'
    _auto = False
    _order = 'partner_id, date_order desc'
    order_id = fields.Many2one(
        string=u'Sales Order',
        comodel_name='sale.order',
        ondelete='set null', 
        required=True
    )
    date_order = fields.Datetime(
        string=u'Order Date',
    )
    partner_id = fields.Many2one(
        string=u'Customer',
        comodel_name='res.partner',
        required=True,
    )
    user_id = fields.Many2one(
        string=u'Salesperson',
        comodel_name='res.users',
    )
    product_id = fields.Many2one(
        string=u'Product',
        comodel_name='product.product',
        required=True,
    )
    currency_id = fields.Many2one(string="Currency", comodel_name="res.currency")
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0)

    price_tax = fields.Monetary(string='Taxes', digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Monetary(string='Subtotal', digits=dp.get_precision('Product Price'))
    price_total = fields.Monetary(string='Total', digits=dp.get_precision('Product Price'))
    cogs_amount = fields.Monetary(string='COGS', digits=dp.get_precision('Product Price'))
    total_cost = fields.Monetary(string='Total Cost', digits=dp.get_precision('Product Price'))
    gross_profit = fields.Monetary(string='Gross Profit', digits=dp.get_precision('Product Price'))

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'sale_history')
        self._cr.execute("""
            CREATE VIEW sale_history AS (
                SELECT sol.id as id, sol.order_id, so.date_order, so.partner_id, so.user_id, sol.currency_id,
                    sol.product_id, sol.product_uom_qty, sol.price_unit, sm.price_unit as cogs_amount, 
                    sol.discount, sol.price_tax, sol.price_subtotal, sol.price_total, 
                    sm.product_qty * sm.price_unit as total_cost,
                    sol.price_total - (sm.product_qty * sm.price_unit) as gross_profit 
                FROM sale_order so
                JOIN sale_order_line sol on so.id = sol.order_id 
                JOIN product_product p on p.id = sol.product_id
                LEFT JOIN procurement_order po on po.sale_line_id = sol.id
                LEFT JOIN stock_move sm on sm.procurement_id = po.id
                WHERE so.state not in ('draft', 'cancel')
                ORDER BY so.date_order)
            """)