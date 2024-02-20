from odoo import api, fields, models
from odoo.tools import pycompat, ustr


class MailServer(models.Model):
    _inherit = "ir.mail_server"

    custom_headers = fields.Char(
        string="Custom headers",
        help="Custom headers to use with all messages. Separate different keys with comma: "
        "'X-Example1: value1, X-Example2: value2'",
    )

    @api.model
    def send_email(
        self,
        message,
        mail_server_id=None,
        smtp_server=None,
        smtp_port=None,
        smtp_user=None,
        smtp_password=None,
        smtp_encryption=None,
        smtp_ssl_certificate=None,
        smtp_ssl_private_key=None,
        smtp_debug=False,
        smtp_session=None,
    ):
        if mail_server_id:
            mail_server = self.browse([mail_server_id])
            if mail_server and mail_server.custom_headers:
                custom_headers = dict(
                    x.split(":") for x in mail_server.custom_headers.split(",")
                )
                for key, value in custom_headers.items():
                    message[pycompat.to_text(ustr(key))] = value

        return super().send_email(
            message,
            mail_server_id,
            smtp_server,
            smtp_port,
            smtp_user,
            smtp_password,
            smtp_encryption,
            smtp_debug,
            smtp_session,
        )
