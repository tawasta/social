import ast

from odoo import api, fields, models
from odoo.tools.mimetypes import guess_mimetype


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    attachment_file_type = fields.Selection(
        selection=lambda self: self._get_attachment_file_type(), default="all"
    )

    attachment_file_type_exist = fields.Boolean(
        default=lambda self: self._get_attachment_file_type_exist()
    )

    @api.model
    def _get_attachment_file_type(self):
        value_list = self.env["ir.config_parameter"].get_param(
            "attachment_file_type_list", False
        )
        # Use for example this parameter: [("all", "All"), ("pdf", "PDF")]

        def check_is_list(string):
            try:
                return isinstance(ast.literal_eval(string), list)
            except SyntaxError:
                return False

        if not value_list:
            return [("all", "All")]

        if check_is_list(value_list):
            value_list = ast.literal_eval(value_list)

        return value_list

    def _get_attachment_file_type_exist(self):
        value = self.env["ir.config_parameter"].get_param(
            "attachment_file_type_list", False
        )

        return value

    def product_bom_attachments(self, product_ids):
        product_list = []

        for product in product_ids:
            bom_ids = product.bom_ids
            for bom in bom_ids:
                product_list += self.get_sub_lines(bom, 0)

        return product_list

    def get_sub_lines(self, current_bom, level):
        lines = []

        company = self.record_company_id
        upper_level = company and company.recursive_level or False

        for bom_line in current_bom.bom_line_ids:
            product_id = bom_line.product_id

            lines.append(product_id)

            if bom_line.child_bom_id:
                child_bom = product_id.bom_ids and product_id.bom_ids[0]
                level += 1

                if level < upper_level:
                    lines += self.get_sub_lines(child_bom, level)
        return lines

    def get_product_bom_attachments(self, order):
        return [line.product_id for line in order.order_line]

    @api.depends("res_ids", "model", "attachment_file_type")
    def _compute_display_object_attachment_ids(self):
        """Redefined function"""
        for composer in self:
            res_ids = self._evaluate_res_ids()
            model = self.model

            company = self.record_company_id
            company_models = (
                company
                and company.recursive_attachment_model_ids
                and company.recursive_attachment_model_ids.mapped("model")
                or []
            )

            if model in company_models:
                order = self.env[model].browse(res_ids)

                product_ids = self.get_product_bom_attachments(order)
                bom_product_ids = self.product_bom_attachments(product_ids)

                all_products = product_ids + bom_product_ids
                all_product_templates = [p.product_tmpl_id for p in all_products]

                all_product_ids = [p.id for p in all_products]
                all_product_template_ids = [t.id for t in all_product_templates]

                domain = [
                    "|",
                    "|",
                    "&",
                    ("res_model", "=", model),
                    ("res_id", "in", res_ids),
                    "&",
                    ("res_model", "=", "product.product"),
                    ("res_id", "in", all_product_ids),
                    "&",
                    ("res_model", "=", "product.template"),
                    ("res_id", "in", all_product_template_ids),
                ]

                attachment_ids = self.env["ir.attachment"].search(domain)
                filtered_attachment_ids = self.env["ir.attachment"]

                file_type = composer.attachment_file_type

                if file_type != "all":
                    for attachment in attachment_ids:
                        if guess_mimetype(attachment.raw).endswith(
                            file_type
                        ) or attachment.name.endswith(file_type):
                            filtered_attachment_ids |= attachment
                else:
                    filtered_attachment_ids = attachment_ids

                composer.display_object_attachment_ids = filtered_attachment_ids
            elif model and res_ids:
                attachments = self.env["ir.attachment"].search(
                    [
                        ("res_model", "=", model),
                        ("res_id", "in", res_ids),
                    ]
                )
                composer.display_object_attachment_ids = attachments
            else:
                composer.display_object_attachment_ids = False
