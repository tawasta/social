from odoo import _, api, models


class MailTrackingEmail(models.Model):

    _inherit = "mail.tracking.email"

    @api.model
    def create(self, values):
        res = super().create(values)
        self.failure_message_send()
        return res

    def write(self, values):
        res = super().write(values)
        self.failure_message_send()
        return res

    def failure_message_send(self):
        for record in self:
            if record.state in ["error", "rejected", "soft-bounced", "bounced"]:
                # Notify the sender about failed message

                # Construct the message (we could also use an email template here)
                subject = _(
                    "Sending message '{}' to '{}' failed".format(
                        record.name, record.recipient
                    )
                )
                body = _(
                    "Sending message '{}' to '{}' failed: {}".format(
                        record.name, record.recipient, record.error_description
                    )
                )

                mail_message = record.mail_message_id
                if mail_message.res_id and mail_message.model:
                    linked_record = (
                        self.env[mail_message.model]
                        .sudo()
                        .browse([mail_message.res_id])
                    )
                    url = linked_record.get_base_url()
                    url += "/web#id=%d&view_type=form&model=%s" % (
                        linked_record.id,
                        linked_record._name,
                    )

                    body += "<br /><a href='{}'>{}</a>".format(url, url)

                mail_values = {
                    "subject": subject,
                    "body_html": body,
                    "email_from": self.env.ref("base.partnerF_root").email,
                    "email_to": record.sender,
                }

                self.env["mail.mail"].with_context().create(mail_values)
