from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

from datetime import datetime

class SaleOrder(models.Model):
    
    _inherit = ['sale.order']
    
    approved_user_id = fields.Many2one(
        string=u'Approved User',
        comodel_name='res.users',
        ondelete='set null',
        domain=lambda self: [('id', 'in', self.env.user.company_id.user_approval_order.ids)]
    )
    
    _sql_constraints = [
        ('client_order_ref_unique',
         'UNIQUE(client_order_ref)',
         "Customer reference must be unique"),
    ]

class SaleOrderLine(models.Model):
    
    _inherit = ['sale.order.line']

    @api.constrains('price_unit', 'price_total')
    def _check_something(self):
        for record in self:
            sale_history = self.env['sale.history'].search([
                ('partner_id', '=', record.order_id.partner_id.id),
                ('product_id', '=', record.product_id.id),
            ])

            if sale_history:
                last_sale_price = (sale_history[0].price_total / sale_history[0].product_uom_qty)
                current_sale_price = (record.price_total / record.product_uom_qty)
                if last_sale_price > current_sale_price:
                    raise ValidationError("Current sale price is smaller than last sale price {:,}!".format(last_sale_price))
    