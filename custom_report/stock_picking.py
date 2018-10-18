from odoo import api, fields, models, _

class Picking(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
