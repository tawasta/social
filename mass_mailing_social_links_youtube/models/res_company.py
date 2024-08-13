from odoo import models


class ResCompany(models.Model):

    _inherit = "res.company"

    def _get_social_media_links(self):

        self.ensure_one()
        social_media_links = super()._get_social_media_links()
        website_id = self.env["website"].get_current_website()

        social_media_links.update(
            {"social_youtube": website_id.social_youtube or self.social_youtube}
        )

        return social_media_links
