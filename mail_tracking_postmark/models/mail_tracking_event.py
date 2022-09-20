from odoo import fields, models


class MailTrackingEvent(models.Model):
    _inherit = "mail.tracking.event"

    _sql_constraints = [
        (
            "postmark_message_id_unique",
            "UNIQUE(postmark_message_id)",
            "Postmark event IDs must be unique!",
        )
    ]

    postmark_message_id = fields.Char(
        string="Postmark MessageID",
        copy="False",
        readonly=True,
        index=True,
    )

    def _process_data(self, tracking_email, metadata, event_type, state):
        res = super()._process_data(tracking_email, metadata, event_type, state)
        res.update({"postmark_message_id": metadata.get("postmark_message_id", False)})
        return res
