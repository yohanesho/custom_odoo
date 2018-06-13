from odoo import api, fields, models, _

class ProductAttribute(models.Model):
    
    _inherit = ['product.attribute']
    
    type = fields.Selection(
        string=u'Type',
        default='other',
        required=True,
        selection=[('color', 'Colors'), ('other', 'Others')]
    )

class ProductAttributeLine(models.Model):
    
    _inherit = ['product.attribute.line']

    type = fields.Selection(
        string=u'Type',
        default='other',
        required=True,
        selection=[('color', 'Colors'), ('other', 'Others')]        
    )