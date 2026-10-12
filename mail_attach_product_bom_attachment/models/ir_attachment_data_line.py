from odoo import _, fields, models


class IrAttachmentDataLine(models.TransientModel):
    _name = "ir.attachment.data.line"
    _order = "product_level asc"
    _description = "Attachment Data Line"

    attachment_id = fields.Many2one("ir.attachment", string="Attachment")

    file_type_display_name = fields.Char(
        compute=lambda self: self._compute_file_display_names(),
        store=True,
        string="Type",
    )

    file_size_display_name = fields.Char(
        compute=lambda self: self._compute_file_display_names(),
        store=True,
        string="Size",
    )

    file_product_display_name = fields.Char(
        compute=lambda self: self._compute_file_display_names(),
        store=True,
        string="Product",
    )

    is_selected_to_send = fields.Boolean(string="To Send")

    product_level = fields.Integer(default=0)

    def _compute_file_display_names(self):
        for data in self:
            attachment = data.attachment_id
            if attachment.name:
                data.file_type_display_name = attachment.name.split(".")[-1].upper()
            else:
                data.file_type_display_name = False

            def format_bytes(size):
                power = 2**10
                n = 0
                power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
                while size > power:
                    size /= power
                    n += 1
                return round(size, 1), power_labels[n] + _("B")

            if attachment.file_size:
                size, bytes_name = format_bytes(attachment.file_size)
                data.file_size_display_name = f"{size} {bytes_name}"
            else:
                data.file_size_display_name = "{} {}".format(0, _("B"))

            if attachment.res_id and attachment.res_model == "product.product":
                product_id = self.env["product.product"].browse(attachment.res_id)
                if product_id:
                    data.file_product_display_name = (
                        product_id.product_tmpl_id.display_name
                    )
                else:
                    data.file_product_display_name = ""
            elif attachment.res_id and attachment.res_model == "product.template":
                product_id = self.env["product.template"].browse(attachment.res_id)
                if product_id:
                    data.file_product_display_name = product_id.display_name
                else:
                    data.file_product_display_name = ""
            else:
                data.file_product_display_name = ""
