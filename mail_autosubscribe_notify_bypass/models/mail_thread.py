import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _check_autosubscribe_bypass(self):
        """Check if the current model has been configured to bypass
        autosubscribe notifications."""
        company = self.env.user.company_id

        return (
            self._name in company.autosubscribe_bypass_model_ids.mapped("model")
            or company.autosubscribe_bypass_all
        )

    def _message_auto_subscribe_notify(self, partner_ids, template):
        if self._check_autosubscribe_bypass():
            # Add some debugging data and return without calling super()
            records = self.mapped("id")
            partners = self.env["res.partner"].browse(partner_ids).mapped("name")
            msg = _(
                "Bypassing the sending of autosubscribe mail regarding %s "
                "IDs %s to partners %s" % (self._name, records, partners)
            )
            _logger.debug(msg)
            return
        else:
            # If no bypass, fall back to core functionality
            return super(MailThread, self)._message_auto_subscribe_notify(
                partner_ids, template
            )
