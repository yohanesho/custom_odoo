from odoo import api, fields, models

class IrMailServer(models.Model):
    """Represents an SMTP server, able to send outgoing emails, with SSL and TLS capabilities."""
    _inherit = "ir.mail_server"

    @api.multi
    def name_get(self):
        return [(server.id, "(%s)" % server.smtp_user) for server in self]

class XCustomMailGatewayComposer(models.TransientModel):
    """
        Update email_from field in composer box
    """

    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields):
        """ Handle composition mode. Some details about context keys:
            - comment: default mode, model and ID of a record the user comments
                - default_model or active_model
                - default_res_id or active_id
            - reply: active_id of a message the user replies to
                - default_parent_id or message_id or active_id: ID of the
                    mail.message we reply to
                - message.res_model or default_model
                - message.res_id or default_res_id
            - mass_mail: model and IDs of records the user mass-mails
                - active_ids: record IDs
                - default_model or active_model
        """
        result = super(XCustomMailGatewayComposer, self).default_get(fields)
        email = self.env['res.users'].browse(self.env.uid).login
        outgoing_ids = self.env['ir.mail_server'].search([('smtp_user', '=', email)])
        if outgoing_ids:
            for outgoing in outgoing_ids:
                result['mail_server_id'] = outgoing.id

        return result
    @api.onchange('mail_server_id')
    def onchange_mail_server_id(self):
        self.update({
        	'email_from': '%s <%s>' % (self.env['res.users'].browse(self.env.uid).name, self.mail_server_id.smtp_user),
        	'reply_to': self.mail_server_id.smtp_user,
        })
