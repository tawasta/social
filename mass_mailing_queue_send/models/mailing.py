import logging
import math
import threading

from odoo import fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    mail_queue_created = fields.Boolean(
        default=False,
        copy=False,
        help="This mailing is being processed by queue jobs.",
    )

    queue_job_status = fields.Html(
        compute="_compute_queue_job_status",
        string="Mailing status",
    )

    queue_job_ids = fields.One2many(
        comodel_name="queue.job",
        compute="_compute_queue_job_ids",
        string="Queue Jobs",
    )

    def _compute_queue_job_status(self):
        for record in self:
            parts = []

            for job in record.queue_job_ids:
                state = (
                    "success"
                    if job.state == "done"
                    else "warning"
                    if job.state == "started"
                    else "danger"
                    if job.state == "failed"
                    else "info"
                )
                html_class = f"badge rounded-pill bg-{state}"
                parts.append(
                    f"<div>{job.name} <span class='{html_class}'>{state}</span></div>"
                )

            record.queue_job_status = "".join(parts)

    def _compute_queue_job_ids(self):
        QueueJob = self.env["queue.job"].sudo()

        # Pre-fetch all jobs for mass.mailing model
        jobs = QueueJob.search([("model_name", "=", self._name)])

        for mailing in self:
            # Filter: job.records is a recordset; check if mailing is in it
            related = jobs.filtered(lambda j, mailing=mailing: mailing in j.records)
            mailing.queue_job_ids = related

    def action_send_mail(self, res_ids=None):
        """Use queue for sending"""
        if self.mail_queue_created:
            # This mailing is already being processed by queue jobs
            _logger.warning(
                "Mailing '%s' (%s) is already being processed by queue jobs.",
                self.name,
                self.id,
            )
            return

        start_delay = 30
        queue_job = self.env["queue.job"].sudo()

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
                raise UserError(self.env._("There are no recipients selected."))

            batch_limit = 200
            batch_count = math.ceil(len(mailing_res_ids) / batch_limit)
            for _batch in range(0, batch_count):
                if len(mailing_res_ids) > batch_limit:
                    recipients = mailing_res_ids[:batch_limit]
                else:
                    recipients = mailing_res_ids

                # Construct the queue job function string to check for existing jobs
                func_string = f"{str(self)}.action_send_mail_queue({recipients})"
                existing_job = queue_job.search([("func_string", "=", func_string)])
                if existing_job:
                    _logger.warning(
                        "Queue job for mailing '%s' (%s) "
                        "with recipients '%s' already exists. "
                        "Skipping creation of duplicate job.",
                        mailing.name,
                        mailing.id,
                        recipients,
                    )
                    continue

                mailing_res_ids = list(set(mailing_res_ids) - set(recipients))
                job_desc = (
                    f"Send mailing '{mailing.subject}' to {len(recipients)} recipients"
                )
                mailing.with_delay(
                    description=job_desc, eta=start_delay
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
