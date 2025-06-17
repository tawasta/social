import logging

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    contact_list_count = fields.Integer(
        "Total recipients", compute="_compute_recipient_count"
    )
    contact_list_is_synced = fields.Boolean(
        "Contact lists synced", compute="_compute_contact_list_is_synced"
    )
    mass_mailing_recipient_limit = fields.Integer(
        "Recipient limit", compute="_compute_mass_mailing_recipient_limit"
    )

    disable_sending = fields.Boolean(
        "Sending disabled", compute="_compute_disable_sending"
    )

    def _compute_recipient_count(self):
        for record in self:
            record.contact_list_count = sum(
                record.contact_list_ids.mapped("contact_count")
            )

    def _compute_contact_list_is_synced(self):
        for record in self:
            record.contact_list_is_synced = all(
                record.contact_list_ids.mapped("is_synced")
            )

    def _compute_mass_mailing_recipient_limit(self):
        limit = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("mass_mailing_recipient_limit.mass_mailing_recipient_limit")
        )
        for record in self:
            record.mass_mailing_recipient_limit = limit

    def _compute_disable_sending(self):
        for record in self:
            record.disable_sending = record._is_sending_disabled()

    def _is_sending_disabled(self):
        # Overridable check for disabled sending
        self.ensure_one()

        # Recipient amount over the maximum limit
        over_limit = self.contact_list_count > self.mass_mailing_recipient_limit

        # Not synced
        synced = self.contact_list_is_synced

        disabled = over_limit or not synced

        return disabled

    def action_launch(self):
        for record in self:
            if record.disable_sending:
                raise ValidationError(_("Sending is disabled!"))

        return super().action_launch()

    def action_send_mail(self, res_ids=None):
        for record in self:
            if record.disable_sending:
                raise ValidationError(_("Sending is disabled!"))

        return super().action_send_mail(res_ids)

    def action_schedule(self):
        for record in self:
            if record.disable_sending:
                raise ValidationError(_("Sending is disabled!"))

        return super().action_schedule()
