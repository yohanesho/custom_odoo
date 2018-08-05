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

    @api.multi
    def write(self, values):
        if 'attachment_ids' in values and values['attachment_ids']\
            or 'email' in values:
            template_id = self.env.ref('sale.email_template_edi_sale')
            if template_id:
                res = {}
                if values.get('attachment_ids'):
                    res['attachment_ids'] = values.get('attachment_ids')
                if values.get('email'):
                    res['email_from'] = values.get('email')
                template_id.sudo().write(res)

        result = super(res_company, self).write(values)