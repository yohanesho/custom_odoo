from odoo import api, fields, models, _

from datetime import datetime
from itertools import groupby

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    @api.model
    def _scheduler_notif_obsolete_order(self):
        stock_picks = self.env['stock.picking'].search([
            ('state', 'not in', ['done', 'cancel']), 
            ('picking_type_id.code','=', 'incoming'), 
            ('location_id.usage', '=', 'supplier'),
            ('min_date', '<', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('purchase_id', '!=', False)])

        if stock_picks:
            purchase_id = [x['purchase_id'] for x in stock_picks]
            purchase_id.sort(key=lambda x:x['create_uid'])

            for create_uid, orders in groupby(purchase_id,key=lambda x:x['create_uid']):
                body = """
                <h3 style="color: inherit; font-size: 16px; font-family: inherit; margin: 18px 0 9px 0">Hi Mr/Mrs %s,</h3>""" % (create_uid.partner_id.name)
                body += """<p style="font-size: 13px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif; margin: 0px 0px 9px 0px"><font style="font-size: 14px">You have some overdue purchase lead time. Here is the detail:</font></p>
                <table style="max-width: 100%; width: 100%; margin: 0 0 18px 0; background-color: transparent; border-collapse: collapse" border="1px" cellpadding="8px">
                    <thead>
                        <tr>
                            <td style="padding: 8px"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;"><b>Order Reference</b></font></td>
                            <td style="padding: 8px"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;"><b>Order Date</b></font></td>
                            <td style="padding: 8px"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;"><b>Schedule Date</b></font></td>
                            <td style="padding: 8px"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;"><b>Supplier</b></font></td>
                            <td style="padding: 8px"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;"><b>Product</b></font></td>
                            <td style="padding: 8px; text-align: right"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;"><b>Qty Order</b></font></td>
                            <td style="padding: 8px; text-align: right"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;"><b>Qty Received</b></font></td>
                            <td style="padding: 8px; text-align: right"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;"><b>Remaining Qty</b></font></td>
                        </tr>
                    </thead>
                    <tbody>"""

                for order in list(orders):
                    name = order.name
                    date_order = order.date_order
                    date_planned = order.date_planned
                    vendor_name = order.partner_id.name
                    print_order = ''
                    for line in order.order_line:
                        if line.product_qty > line.qty_received:
                            body += """
                        <tr>
                            <td style="padding: 8px"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">%s</font></td>
                            <td style="padding: 8px"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">%s</font></td>
                            <td style="padding: 8px"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">%s</font></td>
                            <td style="padding: 8px"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">%s</font></td>
                            <td style="padding: 8px"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">%s</font></td>
                            <td style="padding: 8px; text-align: right"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">%s</font></td>
                            <td style="padding: 8px; text-align: right"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">%s</font></td>
                            <td style="padding: 8px; text-align: right"><font style="font-size: 12px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">%s</font></td>
                        </tr>""" % ((print_order <> name) and name or '',\
                            (print_order <> name) and date_order or '',\
                            (print_order <> name) and date_planned or '',\
                            (print_order <> name) and vendor_name or '',\
                            line.product_id.display_name, line.product_qty, line.qty_received, line.product_qty - line.qty_received)
                            print_order = name                                
                
                body += """</tbody>
                </table>
                <p style="font-size: 13px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif; margin: 0px 0px 9px 0px"><font style="font-size: 14px">Please follow up your Vendor again to re-schedule next incoming supply.</font></p>
                <p style="font-size: 13px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif; margin: 0px 0px 9px 0px"><font style="font-size: 14px">Thank you.</font></p>"""
                self.message_post(body=body, type="notification", subtype="mt_comment", partner_ids=[create_uid.partner_id.id], suYbject="Overdue Receiving Lead Time")