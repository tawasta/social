from odoo import fields, models

import logging

_logger = logging.getLogger(__name__)

class MailRenderMixin(models.AbstractModel):
    _inherit = "mail.render.mixin"

    def _render_template_postprocess(self, rendered):
        model = self.env.context.get('mail_render_postprocess_model')
        active_model = self.env.context.get('active_model')
        res_ids = list(rendered.keys())
        mailing_mailing = None
        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        if active_model == "mailing.mailing" and active_id:
            mailing_mailing = self.env["mailing.mailing"].search([('id', '=', active_id)], limit=1)
        for res_id, rendered_html in rendered.items():
            base_url = None
            if mailing_mailing:
                base_url = mailing_mailing.get_base_url()
            elif model:
                base_url = self.env[model].browse(res_id).with_prefetch(res_ids).get_base_url()
            rendered[res_id] = self._replace_local_links(rendered_html, base_url)
        return rendered

