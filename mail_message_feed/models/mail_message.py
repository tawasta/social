from odoo import models


class MailMessage(models.Model):
    _inherit = "mail.message"

    def action_view_related_record(self):
        self.ensure_one()

        # Search for an action for this model
        model = self.model
        ctx = self.env.context

        # Supported models in alphabetical order
        if model == "contract.contract":
            xml_id = "contract.action_customer_contract"
        elif model == "project.project":
            xml_id = "project.open_view_project_all_config"
        elif model == "project.task":
            xml_id = "project.project_task_action_from_partner"
        else:
            # Add missing action handling
            xml_id = False

        action = self.env["ir.actions.actions"]._for_xml_id(xml_id)

        # TODO: go straight to form view
        res_id = False
        if self.res_id:
            res_id = self.res_id
        elif ctx.get("res_id"):
            res_id = ctx["res_id"]

        action["domain"] = [("id", "=", res_id)]
        action["res_id"] = res_id

        return action
