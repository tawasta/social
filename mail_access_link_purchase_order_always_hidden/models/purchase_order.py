from odoo import models
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _notify_get_recipients_groups(self, message, model_description, msg_vals=None):
        groups = super()._notify_get_recipients_groups(
            message, model_description, msg_vals=msg_vals
        )

        for group_name, _group_method, group_data in groups:
            group_data["has_button_access"] = False

        return groups
