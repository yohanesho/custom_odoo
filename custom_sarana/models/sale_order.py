from odoo import models, fields, api

class SaleOrder(models.Model):
    
    _inherit = ['sale.order']
    
    approved_user_id = fields.Many2one(
        string=u'Approved User',
        comodel_name='res.users',
        ondelete='set null',
        domain=lambda self: [('id', 'in', self.env.user.company_id.user_approval_order.ids)]
    )
    picking_state = fields.Selection(
        string=u'Picking Status',
        selection=[('no', 'Not yet Deliver'), ('to deliver', 'To Deliver'), ('delivered', 'Fully Delivered')],
        compute='_get_picking_state',
        store=True,
    )
    
    @api.depends('state', 'picking_ids','order_line.qty_delivered')
    def _get_picking_state(self):
        for order in self:
            picking_ids = order.mapped('picking_ids')
            picking_status = [pick.state for pick in picking_ids]

            if order.state not in ('sale', 'done'):
                picking_state = 'no'
            elif any(picking_state in ['draft', 'assigned', 'confirmed'] for picking_state in picking_status):
                picking_state = 'to deliver'
            elif any(picking_state == 'done' for picking_state in picking_status):
                picking_state = 'delivered'
            else:
                picking_state = 'no'

            order.update({'picking_state': picking_state})
            
    _sql_constraints = [
        ('client_order_ref_unique',
         'UNIQUE(client_order_ref)',
         "Customer reference must be unique"),
    ]