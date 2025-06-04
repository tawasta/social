import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def _task_message_auto_subscribe_notify(self, users_per_task):
        # Add some debugging data and return without calling super()
        records = self.mapped("id")
        msg = _(
            f"Bypassing the sending of autosubscribe mail regarding {self._name} "
            f"IDs {records}"
        )
        _logger.debug(msg)
        return
