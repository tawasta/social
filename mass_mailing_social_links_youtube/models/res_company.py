from odoo import models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _get_social_media_links(self):
        self.ensure_one()
        social_media_links = super()._get_social_media_links()

        social_media_links.update({"social_youtube": self.social_youtube})

        return social_media_links
