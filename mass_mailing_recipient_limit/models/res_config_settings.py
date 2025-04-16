from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    mass_mailing_recipient_limit = fields.Integer(
        string="Recipient limit for mass mailing",
        config_parameter="mass_mailing_recipient_limit.mass_mailing_recipient_limit",
        default=2000,
    )
