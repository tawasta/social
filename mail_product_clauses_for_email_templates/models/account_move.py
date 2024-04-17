from odoo import fields, models

from odoo.addons.mail.models import mail_render_mixin


class AccountMove(models.Model):

    _inherit = "account.move"

    email_product_clause_contents = fields.Html(
        string="E-mail Product Clause Contents",
        compute="_compute_email_product_clause_contents",
        store=False,
    )

    def _compute_email_product_clause_contents(self):
        """
        Iterates through all the invoice-related clauses that are linked either
        a) directly to this product, or
        b) to its parent product category. Removes any duplicates and
        puts together a single HTML string that supports jinja variables,
        ready to be embedded into an email template.
        """

        clause_model = self.env["email.product.clause"]

        for move in self:

            domain = [
                "&",
                "|",
                (
                    "id",
                    "in",
                    move.invoice_line_ids.product_id.product_tmpl_id.email_product_clause_ids.ids,  # noqa: B950
                ),
                (
                    "id",
                    "in",
                    move.invoice_line_ids.product_id.product_tmpl_id.categ_id.email_product_clause_ids.ids,  # noqa: B950
                ),
                ("ir_model_ids.model", "=", "account.move"),
            ]

            clauses = clause_model.with_context(lang=move.partner_id.lang).search_read(
                domain=domain, fields=["clause_contents"], order="sequence ASC"
            )

            separator = "<br/>"

            combined_contents = separator.join(c["clause_contents"] for c in clauses)

            move.email_product_clause_contents = (
                mail_render_mixin.jinja_template_env.from_string(
                    combined_contents
                ).render(
                    {
                        "objects": move,
                        "o": move,
                    }
                )
            )
