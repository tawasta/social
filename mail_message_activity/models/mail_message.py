from datetime import timedelta

from odoo import _, fields, models


class MailMessage(models.Model):

    _inherit = "mail.message"

    def _mail_message_auto_activity(self, record):
        self.ensure_one()

        subtype_id = self.env.ref("mail.mt_comment")
        if (
            self.author_id != record.user_id.partner_id
            and self.message_type == "comment"
            and self.subtype_id == subtype_id
        ):
            # Auto-create a new activity
            activity_values = {
                "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                # TODO: configurable deadline
                "date_deadline": fields.Datetime.today() + timedelta(2),
                "summary": _("Check messages from partner"),
                "user_id": record.user_id.id,
                "res_model_id": self.env["ir.model"]
                .sudo()
                .search([("model", "=", record._name)])
                .id,
                "res_id": record.id,
            }
            desc = _("Create activity for {}".format(record.name))
            self.env["mail.activity"].sudo().with_delay(description=desc).create(
                activity_values
            )
