from odoo import models


class MailServer(models.Model):
    _inherit = "ir.mail_server"

    def _tracking_headers_add(self, tracking_email_id, headers):
        headers = super()._tracking_headers_add(tracking_email_id, headers)
        headers = headers or {}
        headers["X-PM-Metadata-odoo_db"] = self.env.cr.dbname
        headers["X-PM-Metadata-tracking_email_id"] = tracking_email_id

        return headers
