from odoo import models
from odoo.tools.misc import clean_context


class MailingMailing(models.Model):
    _inherit = "mailing.mailing"

    def action_duplicate(self):
        # Limited senders have no create right on mailings, so that they can't
        # start mailings without recipients from scratch. A duplicate keeps the
        # recipients set by an Email Marketing user, so it is created in sudo
        # once the sender is known to be allowed to read the original. The
        # client's default_* context keys are dropped so that they can't fill
        # fields of the copy with superuser rights.
        if self.env.user.has_group(
            "mass_mailing_limited_rights_sender_group."
            "group_mass_mailing_limited_sender"
        ):
            self.check_access_rule("read")
            # Replacing the whole context is intended: kwargs would only merge
            # and keep the default_* keys
            # pylint: disable=context-overridden
            mailing_sudo = self.sudo().with_context(clean_context(self.env.context))
            return super(MailingMailing, mailing_sudo).action_duplicate()

        return super().action_duplicate()
