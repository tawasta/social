# -*- coding: utf-8 -*-
from odoo import models, api


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.multi
    def _message_add_suggested_recipient(
            self, result, partner=None, email=None, reason=''):
        return result
