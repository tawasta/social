from odoo import _, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

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

    is_selected_to_send = fields.Boolean(default=True, string="To Send")

    product_level = fields.Integer(default=0)

    def _compute_file_display_names(self):
        for attachment in self:
            if attachment.name:
                attachment.file_type_display_name = attachment.name.split(".")[
                    -1
                ].upper()
            else:
                attachment.file_type_display_name = False

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
                attachment.file_size_display_name = f"{size} {bytes_name}"
            else:
                attachment.file_size_display_name = "{} {}".format(0, _("B"))

            if attachment.res_id and attachment.res_model == "product.product":
                product_id = self.env["product.product"].browse(attachment.res_id)
                if product_id:
                    attachment.file_product_display_name = (
                        product_id.product_tmpl_id.display_name
                    )
                else:
                    attachment.file_product_display_name = ""
            elif attachment.res_id and attachment.res_model == "product.template":
                product_id = self.env["product.template"].browse(attachment.res_id)
                if product_id:
                    attachment.file_product_display_name = product_id.display_name
                else:
                    attachment.file_product_display_name = ""
            else:
                attachment.file_product_display_name = ""
