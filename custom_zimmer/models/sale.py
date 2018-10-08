from odoo import models, fields, api

class sale_order(models.Model):
    _inherit = ['sale.order']
    
    send_quotation = fields.Boolean(string=u'Send Quotation', default=False,)
    
    task_id = fields.Many2one(
        string=u'task_id',
        comodel_name='project.task',
        ondelete='set null',
    )
    
    @api.multi
    def action_create_task(self):
        orders = self.filtered(lambda s: s.state == 'sale')
        for order in orders:
            if len(orders) > 0:
                res = {
                    'project_id': self.env.ref('custom_zimmer.project_proforma_invoice').id,
                    'priority': 0,
                    'user_id': self.env.ref('account.group_account_user').users.filtered(lambda s: s.id != 1)[0].id,
                    'name':'Pro-forma invoice request %s' % order.name,
                    'partner_id': order.partner_id.id,
                    'description': 'Pro-forma invoice request %s, partner: %s, within amount: %s' % (order.name, order.partner_id.name, order.amount_total),
                }
                order.write({'task_id': self.env['project.task'].create(res).id})

class sale_order_line(models.Model):
    _inherit = ['sale.order.line']
    
    invoice_after_tax_amount = fields.Float(string=u'invoice_tax_amount',compute='_compute_invoice_after_tax_amount')

    def _compute_invoice_after_tax_amount(self):
        for line in self:
            if line.invoice_lines:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                if line.invoice_lines[0].invoice_line_tax_ids:
                    taxes = line.invoice_lines[0].invoice_line_tax_ids[0].compute_all(price, line.order_id.currency_id, line.qty_invoiced, product=line.product_id, partner=line.order_id.partner_id)
                    line.update({'invoice_after_tax_amount': taxes['total_included'],})
                else:
                    line.update({'invoice_after_tax_amount': line.qty_invoiced * price,})

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.onchange('advance_payment_method')
    def onchange_advance_payment_method(self):
        if self.advance_payment_method == 'percentage':
            order = self.env['sale.order'].browse(self._context.get('active_ids'))[0]
            return {'value': {'amount': order.downpayment}}
        return {}