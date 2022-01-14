##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class MassMailingList(models.Model):
    # 1. Private attributes
    _inherit = "mailing.list"

    # 2. Fields declaration
    # default=lambda self: self.env["ir.config_parameter"].get_param(
    #     "mass_mailing_list_limit.default_mailing_list_limit"
    # ),
    mailing_list_limit = fields.Integer(
        "Contacts Limit", help="Maximum number of contacts for the mailing list."
    )
    room_available = fields.Integer(
        "Available room on list", store=True, readonly=True, compute="_compute_room"
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.depends("mailing_list_limit", "contact_ids.list_ids")
    def _compute_room(self):
        print("COMPUTE")
        for mailing_list in self:
            print(mailing_list.name)
            print(len(mailing_list.contact_ids))
            mailing_list.room_available = mailing_list.mailing_list_limit - len(
                mailing_list.contact_ids
            )

    # 5. Constraints and onchanges
    @api.constrains("mailing_list_limit", "room_available")
    def _check_contacts_limit(self):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        for mailing_list in self:
            if mailing_list.room_available < 0:
                raise ValidationError(
                    _(
                        "Mailing list: %s is full. Remove mailing list contacts or increase the mailing list limit.",
                        mailing_list.name,
                    )
                )

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
