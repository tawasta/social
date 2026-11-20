from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _notify_get_recipients_groups(self, message, model_description, msg_vals=False):
        groups = super()._notify_get_recipients_groups(
            message, model_description, msg_vals=msg_vals
        )

        for _group_name, _group_method, group_data in groups:
            group_data["has_button_access"] = False

        return groups
