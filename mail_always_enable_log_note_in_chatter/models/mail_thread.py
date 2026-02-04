from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, *args, **kwargs):
        message_type = kwargs.get("message_type", False)
        subtype_xmlid = kwargs.get("subtype_xmlid", False)

        if (
            message_type
            and message_type == "comment"
            and subtype_xmlid
            and subtype_xmlid == "mail.mt_note"
        ):
            return super(MailThread, self.sudo()).message_post(*args, **kwargs)
        else:
            return super().message_post(*args, **kwargs)
