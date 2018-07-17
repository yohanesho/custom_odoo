# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    delivery_street = fields.Char(string=u'Street',)
    delivery_street2 = fields.Char(string=u'Street 2',)
    delivery_city = fields.Char(string=u'City',)
    delivery_zip = fields.Char(string=u'Zip',)
    delivery_phone = fields.Char(string=u'Phone',)
    delivery_mobile = fields.Char(string=u'Mobile',)
    delivery_fax = fields.Char(string=u'Fax',)
    delivery_state_id = fields.Many2one(string=u'State',comodel_name='res.country.state',)
    delivery_country_id = fields.Many2one(string=u'Country',comodel_name='res.country',)
    credit_limit = fields.Monetary(string='Credit Limit', help="Set credit limit using base currency.")

    credit_limit_status = fields.Selection(selection=[('open', 'Open'), ('over', 'Over Credit Limit')], compute='_get_credit_limit_state',)

    @api.one
    def _get_credit_limit_state(self):
        if self and self.credit_limit > 0:
            self.credit_limit_status = 'over' if self.credit_limit < self.credit else 'open'