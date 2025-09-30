import logging

from odoo import models

_logger = logging.getLogger(__name__)


class MailServer(models.Model):
    _inherit = "ir.mail_server"

    def _prepare_email_message(self, message, smtp_session):
        # Replace To, Cc and Bcc headers with lowercase versions
        to_addr = (message.get("To") or "").strip().lower()
        if "To" in message:
            message.replace_header("To", to_addr)
        else:
            message["To"] = to_addr

        cc_addr = (message.get("Cc") or "").strip().lower()
        if "Cc" in message:
            message.replace_header("Cc", cc_addr)
        else:
            message["Cc"] = cc_addr

        bcc_addr = (message.get("Bcc") or "").strip().lower()
        if "Bcc" in message:
            message.replace_header("Bcc", bcc_addr)
        else:
            message["Bcc"] = bcc_addr

        validated_to = self.env.context.get("send_validated_to")

        if validated_to:
            new_validated_to = [v.lower() for v in (validated_to or [])]
            self = self.with_context(send_validated_to=new_validated_to)

        res = super()._prepare_email_message(message, smtp_session)

        return res
