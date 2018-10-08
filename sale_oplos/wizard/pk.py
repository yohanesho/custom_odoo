from odoo import api, fields, models, _
import time
import csv
from odoo.modules import get_modules, get_module_path
from odoo.exceptions import UserError

class efaktur_pk_wizard(models.TransientModel):
    _inherit = 'vit.efaktur_pk'


    def baris6(self, headers, csvwriter, line):
        if line.oplos_template_id:
            harga_total = line.oplos_template_id.list_price * line.quantity
            KD_JENIS_TRANSAKSI = line.oplos_template_id.ace_code or ''
            FG_PENGGANTI = line.oplos_template_id.name_get()[0][1] or ''
            NOMOR_FAKTUR = line.oplos_template_id.list_price
        else:
            harga_total = line.price_unit * line.quantity
            KD_JENIS_TRANSAKSI = line.product_id.default_code or ''
            FG_PENGGANTI = line.product_id.name or ''
            NOMOR_FAKTUR = line.price_unit
        dpp = harga_total
        ppn = dpp*0.1 #TODO ambil dari Tax many2many

        data = {
            'FK': 'OF',
            'KD_JENIS_TRANSAKSI': KD_JENIS_TRANSAKSI,
            'FG_PENGGANTI': FG_PENGGANTI,
            'NOMOR_FAKTUR': NOMOR_FAKTUR,
            'MASA_PAJAK': line.quantity ,
            'TAHUN_PAJAK': harga_total,
            'TANGGAL_FAKTUR': line.discount or 0,
            'NPWP': dpp,
            'NAMA': ppn,
            'ALAMAT_LENGKAP': '0',
            'JUMLAH_DPP': '0',
            'JUMLAH_PPN': '',
            'JUMLAH_PPNBM': '',
            'ID_KETERANGAN_TAMBAHAN': '',
            'FG_UANG_MUKA': '',
            'UANG_MUKA_DPP': '',
            'UANG_MUKA_PPN': '',
            'UANG_MUKA_PPNBM': '',
            'REFERENSI': ''
        }
        csvwriter.writerow([data[v] for v in headers])