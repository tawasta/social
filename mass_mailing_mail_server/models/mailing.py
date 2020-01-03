# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
import threading
from ast import literal_eval
from odoo.exceptions import UserError


class MailMail(models.Model):

    _inherit = 'mail.mass_mailing'

    @api.model
    def _get_default_mail_server_id(self):
        server_id = self.env['ir.config_parameter'].sudo().get_param('mass_mailing.mail_server_id')
        try:
            server_id = literal_eval(server_id) if server_id else False
            return self.env['ir.mail_server'].search([('id', '=', server_id)]).id
        except ValueError:
            return False

    mail_server_id = fields.Many2one('ir.mail_server', string='Mail Server',
        default=_get_default_mail_server_id,
        help="Use a specific mail server in priority. Otherwise Odoo relies on the first outgoing mail server available (based on their sequencing) as it does for normal mails.")

    def send_mail(self):
        author_id = self.env.user.partner_id.id
        for mailing in self:
            # instantiate an email composer + send emails
            res_ids = mailing.get_remaining_recipients()
            if not res_ids:
                raise UserError(_('Please select recipients.'))

            # Convert links in absolute URLs before the application of the shortener
            mailing.body_html = self.env['mail.template']._replace_local_links(mailing.body_html)

            composer_values = {
                'author_id': author_id,
                'attachment_ids': [(4, attachment.id) for attachment in mailing.attachment_ids],
                'body': mailing.convert_links()[mailing.id],
                'subject': mailing.name,
                'model': mailing.mailing_model,
                'email_from': mailing.email_from,
                'record_name': False,
                'composition_mode': 'mass_mail',
                'mass_mailing_id': mailing.id,
                'mailing_list_ids': [(4, l.id) for l in mailing.contact_list_ids],
                'no_auto_thread': mailing.reply_to_mode != 'thread',
                'template_id': None,
                'mail_server_id': mailing.mail_server_id.id,
            }

            if mailing.reply_to_mode == 'email':
                composer_values['reply_to'] = mailing.reply_to

            composer = self.env['mail.compose.message'].with_context(active_ids=res_ids).create(composer_values)
            composer.with_context(active_ids=res_ids).send_mail(auto_commit=True)
            mailing.state = 'done'
        return True