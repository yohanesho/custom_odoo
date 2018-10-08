# -*- coding: utf-8 -*-
from odoo import http

# class Dev41SuratPengantarBarangCiti(http.Controller):
#     @http.route('/dev_41_surat_pengantar_barang_citi/dev_41_surat_pengantar_barang_citi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dev_41_surat_pengantar_barang_citi/dev_41_surat_pengantar_barang_citi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dev_41_surat_pengantar_barang_citi.listing', {
#             'root': '/dev_41_surat_pengantar_barang_citi/dev_41_surat_pengantar_barang_citi',
#             'objects': http.request.env['dev_41_surat_pengantar_barang_citi.dev_41_surat_pengantar_barang_citi'].search([]),
#         })

#     @http.route('/dev_41_surat_pengantar_barang_citi/dev_41_surat_pengantar_barang_citi/objects/<model("dev_41_surat_pengantar_barang_citi.dev_41_surat_pengantar_barang_citi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dev_41_surat_pengantar_barang_citi.object', {
#             'object': obj
#         })