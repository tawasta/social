from odoo import fields, models

import logging

_logger = logging.getLogger(__name__)

class MailRenderMixin(models.AbstractModel):
    _inherit = "mail.render.mixin"

    def _render_template_postprocess(self, rendered):
        if self.env.context.get("active_model") == "mailing.mailing":
            self = self.with_context(mail_render_postprocess_model="mailing.mailing")
        return super(MailRenderMixin, self)._render_template_postprocess(rendered)
