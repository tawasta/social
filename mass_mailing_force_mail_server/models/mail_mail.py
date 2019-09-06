# -*- coding: utf-8 -*-
from odoo import models, api, _


class MailMail(models.Model):

    _inherit = 'mail.mail'

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):
        """
        Send mass mailing mails using another mail server
        """

        mail_server_id = self.env.ref(
            'mass_mailing_force_mail_server.mail_server_bulk_mail')

        if not mail_server_id:
            # The required mail server instance is deleted
            raise Exception(
                _("Error while sending mass mail!\n"
                  "Please remove or reinstall "
                  "mass_mailing_force_mail_server")
            )

        for record in self:
            if record.mailing_id:
                record.mail_server_id = mail_server_id.id

        return super(MailMail, self).send(auto_commit, raise_exception)