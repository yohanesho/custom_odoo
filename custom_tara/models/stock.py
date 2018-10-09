from odoo import models, fields, api, _
from odoo.exceptions import UserError

from datetime import datetime

class stock_picking(models.Model):
    _inherit = 'stock.picking'

    order_id = fields.Many2one('sale.order', compute='_get_sale_order', string='Sale Order', readonly=True)
    lpp = fields.Boolean(string=u'LPP', compute='_get_sale_order', readonly=True,)
    force_credit_limit = fields.Boolean(string=u'Force Credit Limit',default=False, track_visibility='onchange')
    force_uid = fields.Many2one(string=u'Forced Credit Limit By',comodel_name='res.users',ondelete='cascade', track_visibility='onchange')
    force_date = fields.Datetime(string=u'Force Date', track_visibility='onchange')
    credit_limit_state = fields.Selection(string=u'Credit Limit Status',
        selection=[('open', 'Open'), ('over', 'Over Limit'), ('confirmed', 'Forced Credit Limit')],
        compute='_get_credit_limit_state',
    )

    @api.one
    def _get_sale_order(self):
        sale_order = self.env['sale.order'].search([('procurement_group_id', '=', self.group_id.id)])
        if sale_order:
            self.order_id = sale_order[0].id
            self.lpp = sale_order[0].lpp

    @api.one
    def _get_credit_limit_state(self):
        if self.force_credit_limit:
            self.credit_limit_state = 'confirmed'
            return 

        if self.picking_type_id.code == 'outgoing' and self.location_dest_id.usage == 'customer' and self.state not in ['done', 'cancel'] and not self.force_credit_limit:
            if self.partner_id and self.partner_id.credit_limit > 0:
                if self.order_id.amount_total:
                    open_credit = self.partner_id.credit + self.order_id.amount_total
                    partner_limit = self.partner_id.credit_limit
                    if partner_limit < open_credit:
                        self.credit_limit_state = 'over'
                        return
            self.credit_limit_state = 'open'

    @api.multi
    def do_new_transfer(self):
        for pick in self:
            pick._get_credit_limit_state()
            
            if pick.credit_limit_state == 'over' and not self.force_credit_limit:
                if self.user_has_groups('stock.group_stock_manager') or self.user_has_groups('sales_team.group_sale_manager'):
                    pick.update({
                        'force_credit_limit': True,
                        'force_uid': self.env.user.id,
                        'force_date': datetime.now()
                    })
                else:
                    raise UserError(_('You can not validate deliver order cause partner reach credit limit! Partner credit limit is {:,}, remaining limit {:,}. Please contact your Stock Manager or Sales Manager to Validate.'.format(partner_limit, partner_limit - inv.partner_id.credit)))
        
        return super(stock_picking, self).do_new_transfer()