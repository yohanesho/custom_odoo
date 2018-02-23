from odoo import api, fields, models, _

from odoo.addons import decimal_precision as dp

class StockPickingValidator(models.TransientModel):
    _name = 'stock.picking.validator'
    _description = 'Stock Picking Operation Validator'

    pick_id = fields.Many2one(comodel_name='stock.picking')
    line_ids = fields.One2many(comodel_name='stock.picking.validator.line',inverse_name='pick_validator_id')
    picking_type_id = fields.Many2one(comodel_name='stock.picking.type', required=True,)
    picking_type_code = fields.Selection([('incoming', 'Vendors'), ('outgoing', 'Customers'), ('internal', 'Internal')], 'Type of Operation', required=True, related='picking_type_id.code')
    
    @api.model
    def default_get(self, fields):
        res = super(StockPickingValidator, self).default_get(fields)
        if not res.get('pick_id') and self._context.get('active_id'):
            res['pick_id'] = self._context['active_id']
        return res

    @api.one
    def notif_purchase(self):
        for data in self:
            data.pick_id._push_msg_validator(self.line_ids)


class StockPickingValidatorLine(models.TransientModel):
    _name = 'stock.picking.validator.line'

    pick_validator_id = fields.Many2one(comodel_name='stock.picking.validator',ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', ondelete="cascade")
    product_qty = fields.Float('To Do', default=0.0, digits=dp.get_precision('Product Unit of Measure'), required=True)
    ordered_qty = fields.Float('Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'))
    qty_done = fields.Float('Done', default=0.0, digits=dp.get_precision('Product Unit of Measure'))
    msg_validation = fields.Char(string=u'Error Message')
    