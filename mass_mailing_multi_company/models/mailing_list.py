from odoo import fields, models


class MassMailingList(models.Model):
    _inherit = "mailing.list"

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
    )
