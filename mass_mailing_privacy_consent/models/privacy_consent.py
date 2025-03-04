# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class PrivacyConsent(models.Model):
    _inherit = "privacy.consent"
    _mailing_enabled = True
