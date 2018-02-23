# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountConfigSettings(models.TransientModel):
    _inherit = ['account.config.settings']

    rounding_account_id = fields.Many2one(
        string='Default Rounding Account',
        comodel_name='account.account',
        ondelete='cascade',
        help="Account used when invoicing journal entry not balance")

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            self.rounding_account_id = self.company_id.rounding_account_id

        super(AccountConfigSettings, self).onchange_company_id()

    @api.multi
    def set_rounding_account_id(self):
        if self.rounding_account_id and self.rounding_account_id != self.company_id.rounding_account_id:
            self.company_id.write({'rounding_account_id': self.rounding_account_id.id})
        