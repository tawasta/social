from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def get_product_bom_attachments(self, order):
        """If a purchase was created from Work Order, use
        the product from the manufacturing order"""
        # Other models, e.g. sale.order, can also be selected for the recursive
        # attachment search and have no work orders
        if "workorder_ids" not in order._fields:
            return super().get_product_bom_attachments(order)
        # The orders come from the client: the user must be able to read them
        # before their work orders are followed with sudo
        order.check_access("read")
        # sudo: purchase users without manufacturing rights cannot read work
        # orders. Only their products are read, and the BoMs and attachments
        # are still searched with the user's own rights.
        products = order.sudo().workorder_ids.product_id.with_env(self.env)
        if products:
            return list(products)
        return super().get_product_bom_attachments(order)
