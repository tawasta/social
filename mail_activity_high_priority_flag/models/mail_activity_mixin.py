import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class MailActivity(models.AbstractModel):
    _inherit = "mail.activity.mixin"

    contains_high_priority_activities = fields.Boolean(
        compute="_compute_contains_high_priority_activities",
        store=True,
    )

    @api.depends("activity_ids", "activity_ids.high_priority")
    def _compute_contains_high_priority_activities(self):
        """
        Mark the parent record as having high priority activities, for
        searching/filtering
        """
        for record in self:
            record.contains_high_priority_activities = any(
                activity.high_priority for activity in record.activity_ids
            )
