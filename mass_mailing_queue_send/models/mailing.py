##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:
import logging
import math
import threading

# 3. Odoo imports (openerp):
from odoo import fields, models, _
from odoo.exceptions import UserError

# 2. Known third party imports:

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class MassMailing(models.Model):

    # 1. Private attributes
    _inherit = "mailing.mailing"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_send_mail(self, res_ids=None):
        """ Use queue for sending """
        start_delay = 30
        for mailing in self:
            if not res_ids:
                res_ids = mailing._get_remaining_recipients()
            if not res_ids:
                raise UserError(_("There are no recipients selected."))

            batch_limit = 200
            batch_count = math.ceil(len(res_ids) / batch_limit)
            for batch in range(0, batch_count):
                if len(res_ids) > batch_limit:
                    recipients = res_ids[:batch_limit]
                else:
                    recipients = res_ids

                res_ids = list(set(res_ids) - set(recipients))
                job_desc = _("Mass mailing: Sending {} to {} recipients".format(
                    mailing.subject,
                    len(recipients)),
                )
                mailing.with_delay(description=job_desc, eta=start_delay).action_send_mail_queue(recipients)
        return True

    def action_send_mail_queue(self, res_ids):
        """ Odoo-core implementation of action_send_mail (with queue) """
        self.ensure_one()
        mailing = self

        author_id = self.env.user.partner_id.id
        composer_values = {
            "author_id": author_id,
            "attachment_ids": [(4, attachment.id) for attachment in mailing.attachment_ids],
            "body": mailing._prepend_preview(mailing.body_html, mailing.preview),
            "subject": mailing.subject,
            "model": mailing.mailing_model_real,
            "email_from": mailing.email_from,
            "record_name": False,
            "composition_mode": "mass_mail",
            "mass_mailing_id": mailing.id,
            "mailing_list_ids": [(4, l.id) for l in mailing.contact_list_ids],
            "no_auto_thread": mailing.reply_to_mode != "thread",
            "template_id": None,
            "mail_server_id": mailing.mail_server_id.id,
        }
        if mailing.reply_to_mode == "email":
            composer_values["reply_to"] = mailing.reply_to

        composer = self.env["mail.compose.message"].with_context(active_ids=res_ids).create(composer_values)
        extra_context = mailing._get_mass_mailing_context()
        composer = composer.with_context(active_ids=res_ids, **extra_context)
        # auto-commit except in testing mode
        auto_commit = not getattr(threading.currentThread(), "testing", False)
        composer.send_mail(auto_commit=auto_commit)
        mailing.write({
            "state": "done",
            "sent_date": fields.Datetime.now(),
            # send the KPI mail only if it"s the first sending
            "kpi_mail_required": not mailing.sent_date,
        })

    # 8. Business methods
