# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Sales Order Line"

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit  - (line.discount or 0.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.depends('price_unit', 'discount')
    def _get_price_reduce(self):
        for line in self:
            line.price_reduce = line.price_unit - line.discount


    price_reduce = fields.Monetary(compute='_get_price_reduce', string='Price Reduce', readonly=True, store=True)
    discount = fields.Float(string='Discount', digits=dp.get_precision('Discount'), default=0.0)

    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        self.discount = 0.0
        if not (self.product_id and self.product_uom and
                self.order_id.partner_id and self.order_id.pricelist_id and
                self.order_id.pricelist_id.discount_policy == 'without_discount' and
                self.env.user.has_group('sale.group_discount_per_so_line')):
            return

        context_partner = dict(self.env.context, partner_id=self.order_id.partner_id.id)
        pricelist_context = dict(context_partner, uom=self.product_uom.id, date=self.order_id.date_order)

        price, rule_id = self.order_id.pricelist_id.with_context(pricelist_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        new_list_price, currency_id = self.with_context(context_partner)._get_real_price_currency(self.product_id, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)
        new_list_price = self.env['account.tax']._fix_tax_included_price(new_list_price, self.product_id.taxes_id, self.tax_id)
        if price != 0 and new_list_price != 0:
            if self.product_id.company_id and self.order_id.pricelist_id.currency_id != self.product_id.company_id.currency_id:
                # new_list_price is in company's currency while price in pricelist currency
                ctx = dict(context_partner, date=self.order_id.date_order)
                new_list_price = self.env['res.currency'].browse(currency_id).with_context(ctx).compute(new_list_price, self.order_id.pricelist_id.currency_id)
            discount = (new_list_price - price) #/ new_list_price * 100
            if discount > 0:
                self.discount = discount
   