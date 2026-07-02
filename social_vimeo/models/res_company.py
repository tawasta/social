from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    social_vimeo = fields.Char("Vimeo Account")

    def _get_social_media_links(self):
        social_media_links = super()._get_social_media_links()
        social_media_links["social_vimeo"] = self.social_vimeo
        return social_media_links
