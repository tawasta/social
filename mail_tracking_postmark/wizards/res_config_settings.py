import logging

import requests

from odoo import fields, models

_logger = logging.getLogger(__name__)

API_URL = "https://api.postmarkapp.com/webhooks"

WEBHOOK_EVENTS = (
    "Bounce",
    "Delivery",
    "Open",
)

timeout = 600


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    mail_tracking_postmark_api_token = fields.Char(
        string="Postmark API Token",
        config_parameter="postmark.apitoken",
        help="""This token can be found from the API Tokens tab under your
        Postmark server.""",
    )

    def mail_tracking_postmark_register_webhooks(self):
        """Register Postmark webhooks to get mail statuses automatically."""
        mail_tracking = self.env["mail.tracking.email"].sudo()
        headers = mail_tracking._postmark_headers()

        for event in WEBHOOK_EVENTS:
            _logger.info(f"Registering Postmark webhook for {event}")

            # Default transaction stream
            outbound_values = mail_tracking._postmark_hook_data(event, "outbound")
            # Default broadcast stream
            broadcast_values = mail_tracking._postmark_hook_data(event, "broadcast")

            for values in [outbound_values, broadcast_values]:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json=values,
                    timeout=timeout,
                )
                # Assert correct registration
                response.raise_for_status()


    def mail_tracking_postmark_unregister_webhooks(self):
        """Remove existing Postmark webhooks."""
        mail_tracking = self.env["mail.tracking.email"].sudo()
        headers = mail_tracking._postmark_headers()
        _logger.info("Getting current webhooks")

        webhooks = requests.get(
            API_URL,
            headers=headers,
            timeout=timeout,
        )
        webhooks.raise_for_status()

        for webhook in webhooks.json()["Webhooks"]:
            delete_url = "{}/{}".format(API_URL, webhook.get("ID"))
            response = requests.delete(
                delete_url,
                headers=headers,
                timeout=timeout,
            )

            response.raise_for_status()
