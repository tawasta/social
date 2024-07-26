from odoo import models
import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def _notify_security_setting_update(
        self, subject, content, mail_values=None, **kwargs
    ):
        """
        Do not attempt to send notifications when admin password is changed via cron
        """

        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "mail_toggleable_security_setting_update_email.bypass_security_setting_update_emails"
            )
        ):
            _logger.debug("Skipping sending Security Update email")
            return
        else:
            return super()._notify_security_setting_update(
                subject, content, mail_values, **kwargs
            )
