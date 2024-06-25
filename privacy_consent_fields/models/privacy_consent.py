# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PrivacyConsent(models.Model):
    _inherit = "privacy.consent"

    partner_id = fields.Many2one(
        readonly=False,
        track_visibility="onchange",
    )
    activity_id = fields.Many2one(
        readonly=False,
        track_visibility="onchange",
    )
