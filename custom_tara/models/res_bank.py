from odoo import models, fields, api, _
from odoo.exceptions import UserError

class res_bank(models.Model):
    _inherit = 'res.partner.bank'
    
    related_company = fields.Boolean(string=u'Refer to Local Company', default=False,)
    payment_term = fields.Text(string=u'Payment Description',)

    @api.multi
    @api.depends('acc_number', 'bank_name')
    def name_get(self):
        result = []
        for acc in self:
            if acc.bank_id:
                name = '%s - %s' % (acc.bank_name, acc.acc_number)
            else:
                name = '%s' % (acc.acc_number)

            result.append((acc.id, name))
        return result

    @api.onchange('related_company')
    def onchange_related_company(self):
        self.partner_id = self.env.user.company_id.partner_id.id
        self.payment_term = """Pembayaran Harap Ditujukan Ke:
%s
%s
A/C: %s""" % (self.partner_id.name, self.bank_id.name, self.acc_number)