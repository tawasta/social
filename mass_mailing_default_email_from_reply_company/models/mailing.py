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
from odoo import _, fields, models, api
from odoo.exceptions import UserError

# 2. Known third party imports:

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class MassMailing(models.Model):

    # 1. Private attributes
    _inherit = "mailing.mailing"

    email_from = fields.Char(string='Send From', required=True,
                            default=lambda self: self._get_default_parent_company_email())

    reply_to = fields.Char(string='Reply To', compute='_compute_reply_to',
                           readonly=False, store=True,
                           help='Preferred Reply-To Address')

    @api.model
    def _get_default_parent_company_email(self):
        """Hakee pääyrityksen sähköpostiosoitteen moniyritysympäristössä."""
        parent_company = self.env['res.company']._get_main_company()
        return parent_company.email or ''

    @api.depends('reply_to_mode')
    def _compute_reply_to(self):
        """Asettaa 'reply_to' kentän arvon riippuen 'reply_to_mode' kentän arvosta."""
        for mailing in self:
            if mailing.reply_to_mode == 'email' and not mailing.reply_to:
                # Asettaa reply_to kenttään pääyrityksen sähköpostiosoitteen, jos reply_to_mode on 'email'
                mailing.reply_to = self.env['res.company']._get_main_company().email
            elif mailing.reply_to_mode == 'thread':
                # Tyhjentää reply_to kentän, jos reply_to_mode on 'thread'
                mailing.reply_to = False