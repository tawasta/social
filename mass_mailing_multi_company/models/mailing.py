from odoo import fields, models


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
    )
