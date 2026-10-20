from odoo import models


class MailingList(models.Model):
    _inherit = "mailing.list"

    def action_sync(self):
        # Limited senders can't read or create mailing contacts, but sending a
        # mailing syncs its dynamic lists as the current user. The sync is a
        # system operation, done in sudo also by the scheduled sync
        # (mass_mailing_list_sync_automation).
        if self.env.user.has_group(
            "mass_mailing_limited_rights_sender_group."
            "group_mass_mailing_limited_sender"
        ):
            return super(MailingList, self.sudo()).action_sync()

        return super().action_sync()
