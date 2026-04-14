from odoo import fields, models


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    website_id = fields.Many2one(comodel_name="website", string="Website")
