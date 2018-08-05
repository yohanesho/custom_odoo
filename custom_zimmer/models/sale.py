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