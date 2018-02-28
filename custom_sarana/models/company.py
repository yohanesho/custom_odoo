# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = ['res.company']

    rounding_account_id = fields.Many2one(string='Default Rounding Account',comodel_name='account.account',ondelete='cascade',)
    user_approval_order = fields.Many2many(
        string=u'Approved Order',
        comodel_name='res.users',
        relation='user_approve_order_rel',
        column1='company_id',
        column2='user_id',
        domain=lambda self: [('id', 'in', self.env.ref('sales_team.group_sale_manager').users.ids)]
    )