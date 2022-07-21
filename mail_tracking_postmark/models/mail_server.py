import json
from odoo import models


class MailServer(models.Model):
    _inherit = "ir.mail_server"

    def _tracking_headers_add(self, tracking_email_id, headers):
        headers = super()._tracking_headers_add(tracking_email_id, headers)
        headers = headers or {}
        metadata = {
            "odoo_db": self.env.cr.dbname,
            "tracking_email_id": tracking_email_id,
        }
        headers["X-Postmark-Variables"] = json.dumps(metadata)
        return headers
