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
    expired_delivery = fields.Boolean(
        string=u'Expired Delivery',
        compute='_get_expired_delivery',
        default=False,
    )
    
    @api.depends('order_line.procurement_ids')
    def _get_expired_delivery(self):
        for record in self:
            for line in record.order_line:
                expired_delivery = line.mapped('procurement_ids').search([('sale_line_id', '=', line.id), ('date_planned', '<', fields.Datetime.now()), ('state', '!=', 'done')])
                print 'expired_delivery', expired_delivery
                if len(expired_delivery) > 0:
                    record.expired_delivery = True
                    break
    
    _sql_constraints = [
        ('client_order_ref_unique',
         'UNIQUE(client_order_ref)',
         "Customer reference must be unique"),
    ]

class SaleOrderLine(models.Model):
    
    _inherit = ['sale.order.line']

    @api.constrains('price_unit', 'price_total')
    def _validate_last_sale_price(self):
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
    