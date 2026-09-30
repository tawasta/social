from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    recursive_attachment_model_ids = fields.Many2many(
        related="company_id.recursive_attachment_model_ids", readonly=False
    )

    recursive_level = fields.Integer(
        related="company_id.recursive_level", readonly=False
    )
