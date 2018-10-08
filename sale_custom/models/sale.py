import datetime
from datetime import date
# from datetime import timedelta
# from dateutil import relativedelta
# import time

from odoo import models, fields, api, _
from openerp.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
# from openerp.tools.safe_eval import safe_eval as eval
# from openerp.tools.translate import _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.depends('bank_charge', 'amount_untaxed', 'fee')
    def _get_commission(self):
        for order in self:
            order.commission_amount = order.amount_untaxed - (order.bank_charge + order.fee)
            
    @api.depends('partner_id')
    def _partner_order_count(self):
        for sale in self:
            # if sale.state == 'draft':
            # counts = [order.id for order in self.search([('partner_id', '=', sale.partner_id.id),('state','in',('sale','done'))])]
            counts = [order.partner_order_count for order in self.search([('partner_id', '=', sale.partner_id.id)])]        
            # counts = sale.partner_id.sale_order_count
            if counts:
                i = max(counts)
                sale.partner_order_count = i#sale.partner_id.sale_order_count#len(counts)
            
    partner_order_count = fields.Integer(string='Repeat Order', compute='_partner_order_count', store=True, copy=False)
    commission_amount = fields.Float(string='Commission', compute='_get_commission', store=True)
    bank_charge = fields.Float(string='Bank Charge')
    fee = fields.Float(string='Fee')

    @api.multi
    @api.onchange('date_order')
    def onchange_date_order(self):
        date = datetime.datetime.strptime(self.date_order, DEFAULT_SERVER_DATETIME_FORMAT)
        new_date = date + datetime.timedelta(days=14)
        self.validity_date = new_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return {}
    
    # @api.multi
    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     counts = [order.partner_order_count for order in self.search([('partner_id', '=', self.partner_id.id)])]
    #     if counts:
    #         i = max(counts)
    #         self.partner_order_count = i
    #     return {}
    
    # @api.multi
    # def action_confirm(self): 
    #     print 'sssssssssssssssssssssss'       
    #     for order in self:
    #         counts = [sale.partner_order_count for sale in self.search([('partner_id', '=', order.partner_id.id)])]
    #         print 'suksessssssssssssss',counts
    #         if counts:
    #             i = max(counts)
    #             order.partner_order_count = i + 1
    #     res = super(SaleOrder, self).action_confirm()
    #     return res
    @api.multi
    def action_done(self):
        partner_order_count = 0
        print 'teststststse'
        for order in self:
            counts = [sale.partner_order_count for sale in self.search([('partner_id', '=', order.partner_id.id)])]
            if counts:
                i = max(counts)
                partner_order_count = i + 1
        self.write({'state': 'done','partner_order_count' :partner_order_count})

    # @api.multi
    # def action_confirm(self):
    #     print 'teststststst'
    #     for order in self:
    #         counts = [sale.partner_order_count for sale in self.search([('partner_id', '=', order.partner_id.id)])]
    #         if counts:
    #             i = max(counts)
    #             order.partner_order_count = i + 1
    #         order.state = 'sale'
    #         order.confirmation_date = fields.Datetime.now()
    #         if self.env.context.get('send_email'):
    #             self.force_quotation_send()
    #         order.order_line._action_procurement_create()
    #     if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
    #         self.action_done()
    #     return True
    @api.multi
    def action_confirm(self):

        res = super(SaleOrder, self).action_confirm()
        for so in self:
            counts = [sale.partner_order_count for sale in self.search([('partner_id', '=', so.partner_id.id)])]
            print 'counts . . . .. '
            if counts:
                i = max(counts)
                so.partner_order_count = i + 1
        return res