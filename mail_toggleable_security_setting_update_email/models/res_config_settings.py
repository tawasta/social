from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    bypass_security_setting_update_emails = fields.Boolean(
        string="Bypass sending Security Update E-mails",
        config_parameter="mail_toggleable_security_setting_update_email.bypass_security_setting_update_emails",
        default=False,
    )
