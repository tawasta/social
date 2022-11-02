from odoo import _, models


class MailMail(models.Model):
    _inherit = "mail.mail"

    def send(self, *args, **kwargs):
        res = super().send(*args, **kwargs)

        for record in self:
            if record.state == "exception":
                # Notify the sender about failed message
                recipients = record.email_to or ", ".join(
                    r.email or "" for r in record.recipient_ids
                )

                # Construct the message (we could also use an email template here)
                subject = _(
                    "Sending message '{}' to '{}' failed".format(
                        record.subject, recipients
                    )
                )
                body = _(
                    "Sending message '{}' to '{}' failed: {}".format(
                        record.subject, recipients, record.failure_reason
                    )
                )

                if record.res_id and record.model:
                    linked_record = (
                        self.env[record.model].sudo().browse([record.res_id])
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
                    "email_from": self.env.user.company_id.email,
                    "email_to": record.email_from,
                }

                self.env["mail.mail"].with_context().create(mail_values)

        return res
