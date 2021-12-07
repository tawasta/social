from odoo import _, api, fields, models
from odoo.addons.mass_mailing.models.mailing import MASS_MAILING_BUSINESS_MODELS

MASS_MAILING_BUSINESS_MODELS += [
    'privacy.consent'
]

class MassMailing(models.Model):
    _inherit = 'mailing.mailing'