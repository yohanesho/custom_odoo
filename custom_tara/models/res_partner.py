# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    delivery_street = fields.Char(string=u'Street',)
    delivery_street2 = fields.Char(string=u'Street 2',)
    delivery_city = fields.Char(string=u'City',)
    delivery_zip = fields.Char(string=u'Zip',)
    delivery_state_id = fields.Many2one(string=u'State',comodel_name='res.country.state',)
    delivery_country_id = fields.Many2one(string=u'Country',comodel_name='res.country',)
    credit_limit = fields.Monetary(string='Credit Limit', help="Set credit limit using base currency.")

    credit_limit_status = fields.Selection(selection=[('open', 'Open'), ('over', 'Over Credit Limit')], compute='_get_credit_limit_state',)

    @api.one
    def _get_credit_limit_state(self):
        if self and self.credit_limit > 0:
            params = (self.id,)
            query = """select sum(price_total) total from sale_order_line sol
join sale_order so on sol.order_id = so.id and so.state = 'sale' and so.partner_id = %s 
where sol.qty_to_invoice < sol.product_uom_qty """
            self.env.cr.execute(query, params)
            results = self.env.cr.dictfetchall()
            open_order_amount = 0.0
            if results and results[0].get('total'):
                open_order_amount = results[0].get('total')

            open_credit = self.credit + open_order_amount
            partner_limit = self.credit_limit
            if self.credit < open_credit:
                self.credit_limit_status = 'over'
                return
        self.credit_limit_status = 'open'
        