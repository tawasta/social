from odoo import fields, models

from odoo.addons.mail.models import mail_render_mixin


class SaleOrder(models.Model):

    _inherit = "sale.order"

    email_product_clause_contents = fields.Html(
        string="E-mail Product Clause Contents",
        compute="_compute_email_product_clause_contents",
        store=False,
    )

    def _compute_email_product_clause_contents(self):
        """
        Iterates through all the sale-related clauses that are linked either
        a) directly to this product, or
        b) to its parent product category. Removes any duplicates and
        puts together a single HTML string that supports jinja variables,
        ready to be embedded into an email template.
        """

        clause_model = self.env["email.product.clause"]

        for sale in self:

            domain = [
                "&",
                "|",
                (
                    "id",
                    "in",
                    sale.order_line.product_template_id.email_product_clause_ids.ids,
                ),
                (
                    "id",
                    "in",
                    sale.order_line.product_template_id.categ_id.email_product_clause_ids.ids,
                ),
                ("ir_model_ids.model", "=", "sale.order"),
            ]

            clauses = clause_model.with_context(lang=sale.partner_id.lang).search_read(
                domain=domain, fields=["clause_contents"], order="sequence ASC"
            )

            separator = "<br/>"

            combined_contents = separator.join(c["clause_contents"] for c in clauses)

            sale.email_product_clause_contents = (
                mail_render_mixin.jinja_template_env.from_string(
                    combined_contents
                ).render({"objects": sale, "o": sale})
            )
