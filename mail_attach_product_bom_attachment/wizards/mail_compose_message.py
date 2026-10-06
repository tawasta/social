import ast

from odoo import _, api, fields, models
from odoo.models import NewId
from odoo.tools.mimetypes import guess_mimetype


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    attachment_file_type = fields.Selection(
        selection=lambda self: self._get_attachment_file_type(), default="all"
    )

    selectable_attachment_ids = fields.Many2many(
        comodel_name="ir.attachment.data.line",
        string="Object Attachments",
    )

    display_object_attachment_ids = fields.One2many(compute_sudo=True)

    attachment_file_type_exist = fields.Boolean(
        default=lambda self: self._get_attachment_file_type_exist()
    )

    use_bom_attachments = fields.Boolean(
        string="Add attachments from BoM components", default=True
    )

    is_large_file_size = fields.Boolean(
        compute=lambda self: self._compute_is_large_file_size()
    )

    attachment_file_type_ids = fields.Many2many("ir.attachment.file.type")

    @api.onchange("selectable_attachment_ids", "object_attachment_ids")
    def _compute_is_large_file_size(self):
        size_limit = self.record_company_id.attachment_size_limit
        if size_limit:
            size = sum([a.file_size for a in self.object_attachment_ids])
            if size > size_limit:
                self.is_large_file_size = True
            else:
                self.is_large_file_size = False
        else:
            self.is_large_file_size = False

    @api.model
    def _get_attachment_file_type(self):
        value_list = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("attachment_file_type_list", False)
        )
        # Use for example this parameter: [("pdf", "PDF")]

        def check_is_list(string):
            try:
                return isinstance(ast.literal_eval(string), list)
            except SyntaxError:
                return False

        if not value_list:
            return []

        if check_is_list(value_list):
            value_list = ast.literal_eval(value_list)

        value_list.insert(0, ("all", _("All")))

        return value_list

    def _get_attachment_file_type_exist(self):
        value = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("attachment_file_type_list", False)
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

    @api.onchange("selectable_attachment_ids", "use_bom_attachments")
    def onchange_selectable_attachment_ids(self):
        if self.use_bom_attachments:
            attachments_to_send = self.env["ir.attachment"]

            for attach_line in self.selectable_attachment_ids:
                if attach_line.is_selected_to_send:
                    attachments_to_send |= attach_line.attachment_id

            self.write({"object_attachment_ids": [(6, 0, attachments_to_send.ids)]})
        else:
            self.selectable_attachment_ids.unlink()

    @api.onchange("attachment_file_type_ids", "use_bom_attachments")
    def _onchange_file_types_and_use_bom(self):
        """Redefined function"""
        for composer in self:
            composer.display_object_attachment_ids = False

            if not composer.use_bom_attachments:
                composer.object_attachment_ids = False

            if composer.object_attachment_ids and not any(
                isinstance(record.id, NewId)
                for record in composer.object_attachment_ids
            ):
                return

            composer.selectable_attachment_ids = False

            deduplicate_attachments = self.env["ir.attachment"]
            res_ids = self._evaluate_res_ids()
            model = self.model

            company = self.record_company_id
            company_models = (
                company
                and company.sudo().recursive_attachment_model_ids
                and company.sudo().recursive_attachment_model_ids.mapped("model")
                or []
            )

            if model in company_models and composer.use_bom_attachments:
                order = self.env[model].browse(res_ids)

                product_ids = self.get_product_bom_attachments(order)

                bom_product_ids = self.product_bom_attachments(product_ids)

                all_products = product_ids + bom_product_ids
                all_product_templates = [p.product_tmpl_id for p in all_products]

                all_product_ids = [p.id for p in all_products]
                all_product_template_ids = [t.id for t in all_product_templates]

                domain = [
                    "|",
                    "&",
                    ("res_model", "=", "product.product"),
                    ("res_id", "in", all_product_ids),
                    "&",
                    ("res_model", "=", "product.template"),
                    ("res_id", "in", all_product_template_ids),
                ]

                attachment_ids = self.env["ir.attachment"].search(
                    domain, order="product_level desc, id desc"
                )

                filtered_attachment_ids = self.env["ir.attachment"]

                ir_attachment_file_type = self.env["ir.attachment.file.type"]

                if not composer.attachment_file_type_ids:
                    for attachment in attachment_ids:
                        file_type_name = (
                            attachment.name and attachment.name.split(".")[-1]
                        )
                        if file_type_name:
                            ir_attachment_file_type = (
                                self.env["ir.attachment.file.type"]
                                .sudo()
                                .search([("file_type", "=", file_type_name)])
                            )
                            if not ir_attachment_file_type:
                                ir_attachment_file_type = (
                                    self.env["ir.attachment.file.type"]
                                    .sudo()
                                    .create(
                                        {
                                            "name": file_type_name.upper(),
                                            "file_type": file_type_name,
                                        }
                                    )
                                )

                            composer.attachment_file_type_ids |= ir_attachment_file_type

                for file_type_id in composer.attachment_file_type_ids:
                    file_type = file_type_id.file_type
                    if file_type:
                        for attachment in attachment_ids:
                            if (
                                attachment.raw
                                and guess_mimetype(attachment.raw).endswith(file_type)
                            ) or attachment.name.endswith(file_type):
                                attachment._compute_file_display_names()
                                filtered_attachment_ids |= attachment
                    else:
                        filtered_attachment_ids = attachment_ids

                datas = []

                for attach in filtered_attachment_ids:
                    if attach.datas not in datas:
                        datas.append(attach.datas)
                        deduplicate_attachments |= attach

                composer.display_object_attachment_ids = deduplicate_attachments
            else:
                composer.display_object_attachment_ids = False

            composer.create_selectable_lines_and_objects(
                composer, deduplicate_attachments
            )

    def create_selectable_lines_and_objects(self, composer, deduplicate_attachments):
        if composer.display_object_attachment_ids and deduplicate_attachments:
            attachment_data_line_ids = self.env["ir.attachment.data.line"]
            product_level = 0
            deduplicate_attachments = deduplicate_attachments[::-1]
            for attach in deduplicate_attachments:
                attachment_data_line_ids |= self.env["ir.attachment.data.line"].create(
                    {
                        "attachment_id": attach.id,
                        "is_selected_to_send": True,
                        "product_level": product_level,
                    }
                )
                product_level += 1

            attachment_data_line_ids._compute_file_display_names()

            composer.write(
                {"selectable_attachment_ids": [(6, 0, attachment_data_line_ids.ids)]}
            )

            attachments_to_send = self.env["ir.attachment"]

            for attach_line in self.selectable_attachment_ids:
                if attach_line.is_selected_to_send:
                    attachments_to_send |= attach_line.attachment_id

            self.object_attachment_ids = attachments_to_send
