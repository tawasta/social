from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.depends("res_ids", "model")
    def _compute_display_object_attachment_ids(self):
        """Redefined function"""
        for composer in self:
            res_ids = self._evaluate_res_ids()
            model = self.model

            # Add line product attachments if model is SO or PO
            if model in ["sale.order", "purchase.order"]:
                order = self.env[model].browse(res_ids)
                product_ids = order.order_line.mapped("product_id.id")
                template_ids = order.order_line.mapped("product_id.product_tmpl_id.id")

                # (model = res_model AND id = res_id) OR
                # (model = product.product AND id in product_ids) OR
                # (model = product.template AND id in template_ids)
                domain = [
                    "|",
                    "|",
                    "&",
                    ("res_model", "=", model),
                    ("res_id", "in", res_ids),
                    "&",
                    ("res_model", "=", "product.product"),
                    ("res_id", "in", product_ids),
                    "&",
                    ("res_model", "=", "product.template"),
                    ("res_id", "in", template_ids),
                ]

                attachment_ids = self.env["ir.attachment"].search(domain)
                composer.display_object_attachment_ids = attachment_ids
            else:
                composer.display_object_attachment_ids = False
