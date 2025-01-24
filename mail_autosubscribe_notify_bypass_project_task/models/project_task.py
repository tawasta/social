from odoo import _, api, models

import logging

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def _task_message_auto_subscribe_notify(self, users_per_task):
        # Add some debugging data and return without calling super()
        records = self.mapped("id")
        msg = _(
            "Bypassing the sending of autosubscribe mail regarding %s "
            "IDs %s" % (self._name, records)
        )
        _logger.debug(msg)
        return
