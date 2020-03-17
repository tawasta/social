from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    autosubscribe_bypass_model_ids = fields.Many2many(
        comodel_name="ir.model",
        string="Autosubscribe Notification Bypass",
        help=(
            """The selected models will not send the 'You have been
              assigned...' autosubscribe notifications"""
        ),
    )
