# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PrivacyConsent(models.Model):
    _inherit = "privacy.consent"

    partner_id = fields.Many2one(
        "res.partner",
        "Subject",
        required=True,
        readonly=False,
        track_visibility="onchange",
        help="Subject asked for consent.",
    )
    activity_id = fields.Many2one(
        "privacy.activity",
        "Activity",
        readonly=False,
        required=True,
        track_visibility="onchange",
    )
