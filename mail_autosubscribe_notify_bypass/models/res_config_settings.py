from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    autosubscribe_bypass_model_ids = fields.Many2many(
        related="company_id.autosubscribe_bypass_model_ids", readonly=False
    )

    autosubscribe_bypass_all = fields.Boolean(
        related="company_id.autosubscribe_bypass_all", readonly=False
    )
