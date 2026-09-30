from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    recursive_attachment_model_ids = fields.Many2many(
        comodel_name="ir.model",
        string="Get attachments recursively for Models",
        help="The selected models use recursive search "
        "to get attachments to mail template",
    )

    recursive_level = fields.Integer()
