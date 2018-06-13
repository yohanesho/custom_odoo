from odoo import api, fields, models, _

class SupplierLeadTime(models.TransientModel):
    _name = 'purchase.report.lead.time'
    _description = "Supplier Lead Time Report"
    
    start_date = fields.Datetime(string=u'Start Date',default=fields.Datetime.now,)
    end_date = fields.Datetime(string=u'End Date',default=fields.Datetime.now,)
    company_id = fields.Many2one(string=u'Company',comodel_name='res.company',default=lambda self: self.env.user.company_id,)
    filter_partner = fields.Boolean(string=u'Filter Partner',)
    partner_id = fields.Many2many(
        string=u'Vendors',
        comodel_name='res.partner',
        relation='purchase_report_lead_time_filter_partner',
        column1='vendor_id',
        column2='report_id',
    )
    show_details = fields.Boolean(string=u'Print Details',)