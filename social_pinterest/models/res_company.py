from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    social_pinterest = fields.Char("Pinterest Account")

    def _get_social_media_links(self):
        social_media_links = super()._get_social_media_links()
        social_media_links["social_pinterest"] = self.social_pinterest
        return social_media_links
