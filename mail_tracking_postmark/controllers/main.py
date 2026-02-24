import logging

from odoo.http import request, route

from ...mail_tracking.controllers import main
from ...web.controllers.main import ensure_db

_logger = logging.getLogger(__name__)


class MailTrackingController(main.MailTrackingController):
    @route(["/mail/tracking/postmark"], auth="public", type="json", csrf=False)
    def mail_tracking_postmark_webhook(self):
        """Process webhooks from Postmark."""
        ensure_db()

        # Process event
        request.env["mail.tracking.email"].sudo()._postmark_event_process(
            request.jsonrequest,
            self._request_metadata(),
        )
