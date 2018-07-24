from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date, datetime
import odoo.addons.decimal_precision as dp

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _get_domain_user(self):
        ids = self.env.ref('sales_team.group_sale_manager').ids
        return [('groups_id','in', ids)]

    amount_discount = fields.Float(string=u'Discount Amount', default='0.0', states={'draft': [('readonly', False)]})
    amount_discount_total = fields.Float(string=u'Total Discount Amount',compute="get_amount_discount_total",)
    amount_subtotal = fields.Float(string=u'Subtotal Amount',compute="get_amount_discount_total",)
    amount_downpayment = fields.Float(string=u'Subtotal',compute="get_amount_discount_total",)
    amount_text = fields.Char(string=u'Amount Text', compute="get_amount_discount_total")
    
    overdue_status = fields.Integer(string=u'Overdue Status', compute='_get_overdue_status')
    payment_terms = fields.Text(string=u'Bank Description', related='partner_bank_id.payment_term',)
    
    picking_ids = fields.Many2many(
        string=u'Stock Picking',
        comodel_name='stock.picking',
        compute='_get_picking_ids',
    )
    approval_user_id = fields.Many2one(
        string=u'Approval Sign-off',
        comodel_name='res.users',
        ondelete='cascade',
        domain=_get_domain_user,
        states={'draft': [('readonly', False)]}
    )

    @api.one
    def get_amount_discount_total(self):
        self.amount_discount_total = sum([x.amount_discount for x in self.invoice_line_ids])
        self.amount_subtotal = sum([x.price_unit * x.quantity for x in self.invoice_line_ids])
        self.amount_downpayment = sum([((x.price_unit * x.quantity) if x.product_id.type == 'service' and x.price_subtotal < 0 else 0) for x in self.invoice_line_ids])
        if self.currency_id:
            self.amount_text = self.currency_id.amount_to_text(self.amount_total, 'id')[0]

    @api.one
    def _get_picking_ids(self):
        order_line_ids = []
        picking_ids = []
        for line in self.invoice_line_ids:
            order_line_ids += line.sale_line_ids

        for order_line in order_line_ids:
            picking_ids += order_line.order_id.picking_ids.ids

        self.picking_ids = self.env['stock.picking'].search([('id', 'in', picking_ids)])

    def _get_overdue_status(self):
        for record in self:
            if record.state == 'open' and record.residual != 0.0 and datetime.strptime(record.date_due, '%Y-%m-%d').date() < date.today():
                record.overdue_status = 1
            elif record.state == 'paid':
                record.overdue_status = -1
            else:
                record.overdue_status = 0

    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        for line in self.invoice_line_ids:
            line_disc_amount = 0.0
            inv_amount_disc = self.amount_discount
            inv_amount_untaxed = sum([(x.price_unit * (1 - (x.discount or 0.0) / 100.0)) * x.quantity for x in self.invoice_line_ids])
            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            subtotal = price_unit * line.quantity

            if inv_amount_disc > 0 and inv_amount_untaxed > 0:
                amount_discount = (subtotal / inv_amount_untaxed) * inv_amount_disc
                subtotal = subtotal - amount_discount
                price_unit = subtotal / line.quantity
                amount_discount = amount_discount + ((line.price_unit * (line.discount / 100)) * line.quantity)

            taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']
            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']
        return tax_grouped

class account_invoice_line(models.Model):
    
    _inherit = ['account.invoice.line']

    amount_discount = fields.Float(string=u'Discount Amount', compute='_compute_price', default='0.0', readonly=True, store=True)
    price_unit_pcs = fields.Float(string='Unit Price Pcs', digits=dp.get_precision('Product Price'), store=True, readonly=True, compute='_compute_price')
    stock_move_ids = fields.Many2many(
        string=u'Stock Move',
        comodel_name='stock.move',
        compute='_get_stock_move_ids'        
    )

    @api.one
    def _get_stock_move_ids(self):
        move_ids = []
        for sale_order_line in self.sale_line_ids:
            for procurement_id in sale_order_line.procurement_ids:
                move_ids += procurement_id.move_ids.ids
        
        self.stock_move_ids = self.env['stock.move'].search([('id', 'in', move_ids)])
            
    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'invoice_id.date', 'invoice_id.amount_discount')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        amount_discount = 0.0
        inv_amount_disc = self.invoice_id.amount_discount
        inv_amount_untaxed = sum([(x.price_unit * (1 - (x.discount or 0.0) / 100.0)) * x.quantity for x in self.invoice_id.invoice_line_ids])
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        subtotal = price * self.quantity
        taxes = False

        if inv_amount_disc > 0 and inv_amount_untaxed > 0:
            amount_discount = (subtotal / inv_amount_untaxed) * inv_amount_disc
            subtotal = subtotal - amount_discount
            if self.quantity and self.quantity > 0:
                price = subtotal / self.quantity
            amount_discount = amount_discount + ((self.price_unit * (self.discount / 100)) * self.quantity)

        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price
        if self.invoice_id.currency_id and self.invoice_id.company_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.with_context(date=self.invoice_id._get_currency_rate_date()).compute(price_subtotal_signed, self.invoice_id.company_id.currency_id)
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign
        self.amount_discount = amount_discount

        if self.uom_id.id == self.product_id.uom_id.id:
            self.price_unit_pcs = self.price_unit
        else:
            if self.quantity and self.quantity > 0:
                product_qty = self.uom_id._compute_quantity(self.quantity, self.product_id.uom_id)
                self.price_unit_pcs = self.price_unit / product_qty
