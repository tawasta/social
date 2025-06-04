from odoo import fields, models


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    subject = fields.Char(
        help="Subject of your Mailing", required=True, translate=False
    )
