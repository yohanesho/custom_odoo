from odoo import api, fields, models, _

class Picking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'mail.mail']

    @api.multi
    def do_new_transfer(self):
        is_valid = True
        lines = []
        for pick in self:
            for line in pick.pack_operation_ids:
                if ((line.picking_id.picking_type_id.code == 'outgoing' and line.location_dest_id.usage == 'customer')\
                    or (line.picking_id.picking_type_id.code == 'incoming' and line.location_id.usage == 'supplier'))\
                    and line.qty_done > line.product_qty:
                    vals = {
                        'product_id': line.product_id.id,
                        'product_qty': line.product_qty,
                        'ordered_qty': line.ordered_qty,
                        'qty_done': line.qty_done,
                        'msg_validation': 'Qty done cannot be greather than Qty To Do!'
                    }
                    lines.append((0, 0, vals))
                    is_valid = False

            if not is_valid:
                wiz_id = self.env['stock.picking.validator'].create({
                    'pick_id' : pick.id,
                    'picking_type_id': pick.picking_type_id.id,
                    'line_ids': lines
                })
                view = self.env['ir.model.data'].xmlid_to_res_id('custom_sarana.stock_picking_validator_wizard')
                
                return {
                     'name': _('Confirm Validation'),
                     'type': 'ir.actions.act_window',
                     'view_type': 'form',
                     'view_mode': 'form',
                     'res_model': 'stock.picking.validator',
                     'views': [(view, 'form')],
                     'view_id': view,
                     'target': 'new',
                     'res_id': wiz_id.id,
                }

        if is_valid:
            super(Picking, self).do_new_transfer()

    def _push_msg_validator(self, lines):
        body = """
            <div>
                <h2><span style="color: #ff0000;">Receiving Item Failed</span></h2>
                <p>Receiving item: %s for Order: %s, failed because some of quantity processed (done) is greather than quantity to do.</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Item No - Desc </th>
                        <th style="text-align: right;">Qty To Do</th>
                        <th style="text-align: right;">Receiving Qty</th>
                    </tr>
                </thead>""" % (self.name, self.group_id.name)
        body_td = ""
        for line in lines:
            body_td += """<tr>
                        <td>%s</td>
                        <td style="text-align: right;">%s</td>
                        <td style="text-align: right;">%s</td>
                    </tr>
                    """ % (line.product_id.display_name, line.product_qty, line.qty_done)
        body += """
                <tbody>
                    %s
                </tbody>    
            </table>""" % (body_td)

        print 'body: ', body

        user_purchase_manager = self.env.ref('purchase.group_purchase_manager').users
        followers = [x.partner_id.id for x in user_purchase_manager]
        for follower in followers:
            if not self.env['mail.followers'].search([('partner_id', '=', follower), ('res_model', '=', 'stock.picking'), ('res_id', '=', self.id)]):
                self.write({'message_follower_ids': [(0,0, {'res_model':'stock.picking','partner_id':follower})]})
        subject = "Receiving item %s rejected" % (self.name)
        self.message_post(body=body, type="notification", subtype="mt_comment", partner_ids=followers, subject=subject)