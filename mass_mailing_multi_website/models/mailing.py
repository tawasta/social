from odoo import fields, models


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    website_id = fields.Many2one("website", string="Website")
