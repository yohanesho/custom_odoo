# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    delivery_street = fields.Char(string=u'Street',)
    delivery_street2 = fields.Char(string=u'Street 2',)
    delivery_city = fields.Char(string=u'City',)
    delivery_zip = fields.Char(string=u'Zip',)
    delivery_state_id = fields.Many2one(string=u'State',comodel_name='res.country.state',)
    delivery_country_id = fields.Many2one(string=u'Country',comodel_name='res.country',)