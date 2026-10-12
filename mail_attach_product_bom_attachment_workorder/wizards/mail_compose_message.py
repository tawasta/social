from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def get_product_bom_attachments(self, order):
        """If a purchase was created from Work Order, use
        the product from the manufacturing order"""
        if order.workorder_ids:
            return [wo.product_id for wo in order.workorder_ids]
        else:
            return [line.product_id for line in order.order_line]
