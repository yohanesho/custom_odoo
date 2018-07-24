# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_company(models.Model):
    _inherit = ['res.company']

    term_conditions = fields.Binary("Term & Conditions", help="This field using for file pdf or any format to upload company's term and condiotions")
    
    attachment_ids = fields.Many2many(
        'ir.attachment', 
        'terms_company_attachment_rel', 
        'company_id',
        'attachment_id', 
        'Attachments Term & Conditions',
        help="This field using for file pdf or any format to upload company's term and condiotions")
    
    filename = fields.Char()