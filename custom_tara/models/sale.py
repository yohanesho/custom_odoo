from odoo import models, fields, api, _
from odoo.exceptions import UserError

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    amount_discount = fields.Float(string=u'Discount Amount', default='0.0',states={'draft': [('readonly', False)]})
    consignment_ref = fields.Char(string=u'Consignment Reference',)

    # @api.multi
    # def action_confirm(self):
    #     for order in self:
    #         if order.partner_id and order.partner_id.credit_limit > 0:
    #             if order.amount_total:
    #                 open_credit = order.partner_id.credit + order.amount_total
    #                 partner_limit = order.partner_id.credit_limit
    #                 if partner_limit < open_credit:
    #                     raise UserError(_('You can not confirm sales order cause partner reach credit limit! Partner credit limit is {:,}, remaining limit {:,}.'.format(partner_limit, partner_limit - order.partner_id.credit)))

    #         super(sale_order, self).action_confirm()
    
    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()

        invoice_vals = super(sale_order, self)._prepare_invoice()
        invoice_vals['amount_discount'] = self.amount_discount
        
        return invoice_vals
            
class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    amount_discount = fields.Float(string=u'Discount Amount', default='0.0', compute='_compute_amount', readonly=True, store=True)

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'order_id.amount_discount')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            amount_discount = 0.0
            order_amount_disc = line.order_id.amount_discount
            order_amount_untaxed = sum([(x.price_unit * (1 - (x.discount or 0.0) / 100.0)) * x.product_uom_qty for x in line.order_id.order_line])
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            subtotal = price * line.product_uom_qty

            if order_amount_disc > 0 and order_amount_untaxed > 0:
                amount_discount = (subtotal / order_amount_untaxed) * order_amount_disc
                subtotal = subtotal - amount_discount
                price = subtotal / line.product_uom_qty
                amount_discount = amount_discount + ((line.price_unit * (line.discount / 100)) * line.product_uom_qty)

            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
                'amount_discount': amount_discount,
            })

    @api.multi
    def _prepare_invoice_line(self, qty):
        self.ensure_one()

        res = super(sale_order_line, self)._prepare_invoice_line(qty)
        res['amount_discount'] = self.amount_discount
        
        return res