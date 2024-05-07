from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    autosubscribe_bypass_model_ids = fields.Many2many(
        comodel_name="ir.model",
        string="Autosubscribe Notification Bypass Models",
        help="The selected models will not send "
        "'You have been assigned...' autosubscribe notifications",
    )

    autosubscribe_bypass_all = fields.Boolean(
        string="Autosubscribe Notification Bypass All",
        help="No models will send 'You have been assigned...' notifications.",
    )
