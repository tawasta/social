from odoo import _, models
from odoo.tools import format_date


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _notify_by_email_prepare_rendering_context(
        self,
        message,
        msg_vals=False,
        model_description=False,
        force_email_company=False,
        force_email_lang=False,
    ):
        render_context = super()._notify_by_email_prepare_rendering_context(
            message,
            msg_vals,
            model_description=model_description,
            force_email_company=force_email_company,
            force_email_lang=force_email_lang,
        )
        subtitles = [render_context["record"].name]
        # Never show Amount in PO mails
        if self.state not in ["draft", "sent"]:
            if self.date_order:
                subtitles.append(
                    _(
                        "Due\N{NO-BREAK SPACE}%(date)s",
                        date=format_date(
                            self.env,
                            self.date_order,
                            date_format="short",
                            lang_code=render_context.get("lang"),
                        ),
                    )
                )
        render_context["subtitles"] = subtitles
        return render_context
