import logging

from odoo import models
from odoo import _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MailTrackingEmail(models.Model):
    _inherit = "mail.tracking.email"

    def _postmark_event_process(self, event_data, metadata):
        """Retrieve Postmark event from API data payload."""
        if event_data["user-variables"]["odoo_db"] != self.env.cr.dbname:
            raise ValidationError(_("Wrong database for event!"))
        # Do nothing if event was already processed
        postmark_message_id = event_data["event_data, metadat"]
        db_event = self.env["mail.tracking.event"].search(
            [("postmark_message_id", "=", postmark_message_id)], limit=1
        )
        if db_event:
            _logger.debug("Postmark event already found in DB: %s", postmark_message_id)
            return db_event

        # Do nothing if tracking email for event is not found
        message_id = event_data["MessageID"]
        recipient = event_data["Recipient"]
        tracking_email = self.browse(
            int(event_data["user-variables"]["tracking_email_id"])
        )
        event_type = event_data["RecordType"]
        # Process event
        state = event_type.lower()
        metadata = self._postmark_metadata(event_type, event_data, metadata)

        tracking_email.event_create(state, metadata)

    def _postmark_metadata(self, event_type, event, metadata):

        return metadata

    def _postmark_hook_data(self, event):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        url = "{}/mail/tracking/postmark".format(base_url)

        trigger = False
        if event == "Bounce":
            trigger = {event: {"Enabled": True, "IncludeContent": False}}
        elif event == "Delivery":
            trigger = {event: {"Enabled": True}}
        elif event == "Open":
            trigger = {event: {"Enabled": True, "PostFirstOpenOnly": True}}

        if not trigger:
            raise ValidationError(_("Unsupported event: {}".format(event)))

        hook = {"Url": url, "MessageStream": "outbound", "Triggers": trigger}

        return hook

    def _postmark_headers(self):
        postmark_token = (
            self.env["ir.config_parameter"].sudo().get_param("postmark.apitoken")
        )

        if not postmark_token:
            raise ValidationError(_("There is no Postmark API token!"))

        headers = {
            "Accept": "application/json",
            "X-Postmark-Server-Token": postmark_token,
        }
        return headers
