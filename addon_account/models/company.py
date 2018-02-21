# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = "res.company"

    rounding_account_id = fields.Many2one(string='Default Rounding Account',comodel_name='account.account',ondelete='cascade',)