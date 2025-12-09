import logging
import math
import threading

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    mail_queue_created = fields.Boolean(default=False, copy=False)

    """
    queue_job_ids = fields.One2many(
        'queue.job',
        'related_action_id',
        string='Queue Jobs',
        domain=[('related_action', '=', 'mailing.mailing')],
    )
    """

    def action_send_mail(self, res_ids=None):
        """Use queue for sending"""
        start_delay = 30

        # Tell the mailing that queue has already been created to prevent multiple
        # queue jobs from being created for the same mailing.
        self.mail_queue_created = True        
        for mailing in self:
            context_user = mailing.user_id or mailing.write_uid or self.env.user
            mailing = mailing.with_context(
                **self.env["res.users"].with_user(context_user).context_get()
            )
            mailing_res_ids = res_ids or mailing._get_remaining_recipients()
            if not mailing_res_ids:
                raise UserError(_("There are no recipients selected."))

            batch_limit = 200
            batch_count = math.ceil(len(mailing_res_ids) / batch_limit)
            for _batch in range(0, batch_count):
                if len(mailing_res_ids) > batch_limit:
                    recipients = mailing_res_ids[:batch_limit]
                else:
                    recipients = mailing_res_ids

                mailing_res_ids = list(set(mailing_res_ids) - set(recipients))
                job_desc = "Mass mailing: Sending '{}' to {} recipients".format(
                    mailing.subject, len(recipients)
                )
                mailing.with_delay(
                    description=job_desc,
                    eta=start_delay
                ).action_send_mail_queue(recipients)
        return True

    def action_send_mail_queue(self, mailing_res_ids):
        """Odoo-core implementation of action_send_mail (with queue)"""
        self.ensure_one()
        mailing = self

        author_id = self.env.user.partner_id.id
        composer_values = {
            "auto_delete": not mailing.keep_archives,
            # email-mode: keep original message for routing
            "auto_delete_keep_log": mailing.reply_to_mode == "update",
            "author_id": author_id,
            "attachment_ids": [
                (4, attachment.id) for attachment in mailing.attachment_ids
            ],
            "body": mailing._prepend_preview(mailing.body_html, mailing.preview),
            "composition_mode": "mass_mail",
            "email_from": mailing.email_from,
            "mail_server_id": mailing.mail_server_id.id,
            "mailing_list_ids": [(4, clist.id) for clist in mailing.contact_list_ids],
            "mass_mailing_id": mailing.id,
            "model": mailing.mailing_model_real,
            "record_name": False,
            "reply_to_force_new": mailing.reply_to_mode == "new",
            "subject": mailing.subject,
            "template_id": None,
        }
        if mailing.reply_to_mode == "new":
            composer_values["reply_to"] = mailing.reply_to

        composer = (
            self.env["mail.compose.message"]
            .with_context(
                active_ids=mailing_res_ids,
                default_composition_mode="mass_mail",
                **mailing._get_mass_mailing_context(),
            )
            .create(composer_values)
        )
        # auto-commit except in testing mode
        composer._action_send_mail(
            auto_commit=not getattr(threading.current_thread(), "testing", False)
        )
        mailing.write(
            {
                "state": "done",
                "sent_date": fields.Datetime.now(),
                # send the KPI mail only if it's the first sending
                "kpi_mail_required": not mailing.sent_date,
            }
        )
