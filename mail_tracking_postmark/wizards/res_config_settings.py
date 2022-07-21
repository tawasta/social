import logging
import requests

from odoo import fields
from odoo import models

_logger = logging.getLogger(__name__)

API_URL = "https://api.postmarkapp.com/webhooks"

WEBHOOK_EVENTS = (
    "Bounce",
    "Delivery",
    "Open",
)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    mail_tracking_postmark_api_token = fields.Char(
        string="Postmark API Token",
        config_parameter="postmark.apitoken",
        help="This token can be found from the API Tokens tab under your Postmark server.",
    )

    def mail_tracking_postmark_register_webhooks(self):
        """Register Postmark webhooks to get mail statuses automatically."""
        mail_tracking = self.env["mail.tracking.email"].sudo()
        headers = mail_tracking._postmark_headers()

        for event in WEBHOOK_EVENTS:
            _logger.info("Registering Postmark webhook for {}".format(event))
            values = mail_tracking._postmark_hook_data(event)

            response = requests.post(
                API_URL,
                headers=headers,
                json=values,
            )
            # Assert correct registration
            response.raise_for_status()

    def mail_tracking_postmark_unregister_webhooks(self):
        """Remove existing Postmark webhooks."""
        mail_tracking = self.env["mail.tracking.email"].sudo()
        headers = mail_tracking._postmark_headers()
        _logger.info("Getting current webhooks")
        payload = {"MessageStream": "outbound"}

        webhooks = requests.get(API_URL, headers=headers, params=payload)
        webhooks.raise_for_status()

        for webhook in webhooks.json()["Webhooks"]:
            delete_url = "{}/{}".format(API_URL, webhook.get("ID"))
            response = requests.delete(delete_url, headers=headers)

            response.raise_for_status()
