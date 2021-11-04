##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import models
from odoo.tools import safe_eval

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class MassMailingList(models.Model):
    # 1. Private attributes
    _inherit = "mail.mass_mailing.list"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_sync(self):
        """Sync contacts in dynamic lists."""
        Contact = self.env["mail.mass_mailing.contact"].with_context(syncing=True)
        Partner = self.env["res.partner"]
        # Skip non-dynamic lists
        dynamic = self.filtered("dynamic").with_context(syncing=True)
        for one in dynamic:
            sync_domain = [("email", "!=", False)] + safe_eval(one.sync_domain)
            desired_partners = Partner.search(sync_domain)
            # Detach or remove undesired contacts when synchronization is full
            if one.sync_method == "full":
                contact_to_detach = one.contact_ids.filtered(
                    lambda r: r.partner_id not in desired_partners
                )
                one.contact_ids -= contact_to_detach
                contact_to_detach.filtered(lambda r: not r.list_ids).unlink()
            # Add new contacts
            current_partners = one.contact_ids.mapped("partner_id")
            contact_to_list = self.env["mail.mass_mailing.contact"]
            vals_list = []
            for partner in desired_partners - current_partners:
                vals_partner_ids = []
                for val in vals_list:
                    vals_partner_ids.append(val.get("partner_id"))
                vals_partners = self.env["res.partner"].search(
                    [["id", "in", vals_partner_ids]]
                )
                contacts_in_partner = partner.mass_mailing_contact_ids
                # check for duplicate emails from current_partners
                # or vals_partners (recently added)
                # or contact_to_list (mass mailing contacts)
                if (
                    any(
                        old_contact.email.lower() == partner.email.lower()
                        for old_contact in current_partners
                    )
                    or any(
                        old_contact.email.lower() == partner.email.lower()
                        for old_contact in vals_partners
                    )
                    or any(
                        old_contact.email.lower() == partner.email.lower()
                        for old_contact in contact_to_list
                    )
                    or (
                        contacts_in_partner
                        and (
                            any(
                                old_contact.email.lower()
                                == contacts_in_partner[0].email.lower()
                                for old_contact in contact_to_list
                            )
                            or any(
                                old_contact.email.lower()
                                == contacts_in_partner[0].email.lower()
                                for old_contact in vals_partners
                            )
                            or any(
                                old_contact.email.lower()
                                == contacts_in_partner[0].email.lower()
                                for old_contact in current_partners
                            )
                        )
                    )
                ):
                    _logger.info(
                        "Duplicate email already in the mailing list. Skipping..."
                    )
                    continue
                if contacts_in_partner:
                    contact_to_list |= contacts_in_partner[0]
                else:
                    vals_list.append(
                        {"list_ids": [(4, one.id)], "partner_id": partner.id}
                    )
            one.contact_ids |= contact_to_list
            Contact.create(vals_list)
            one.is_synced = True
        # Invalidate cached contact count
        self.invalidate_cache(["contact_nbr"], dynamic.ids)

    # 8. Business methods
