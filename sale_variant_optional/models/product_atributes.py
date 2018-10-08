# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

	
class ProductAttribute(models.Model):
    _inherit = "product.attribute"
    _description = "Product Attribute"

    def _get_default_type_variant(self):
        if self._context.get('default_type_variant'):
            return self._context.get('default_type_variant')
        return False

    type_variant = fields.Selection([('colours','Colours'),('other','Other')], string='Type',default=_get_default_type_variant,)

class ProductAttributeLine(models.Model):
    _inherit = "product.attribute.line"
    type_variant = fields.Selection([('colours','Colours'),('other','Other')], string='Type')