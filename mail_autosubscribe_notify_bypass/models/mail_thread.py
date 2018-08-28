# -*- coding: utf-8 -*-
from odoo import models, api
import logging
_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):

    _inherit = 'mail.thread'

    def _check_autosubscribe_bypass(self):
        '''Check if the current model has been configured to bypass
        autosubscribe notifications.'''
        return self._name in self.env.user.company_id. \
            autosubscribe_bypass_model_ids.mapped('model')

    @api.multi
    def _message_auto_subscribe_notify(self, partner_ids):
        if self._check_autosubscribe_bypass():
            # Add some debugging data and return without calling super()
            records = self.mapped('id')
            partners = self.env['res.partner'] \
                .browse(partner_ids).mapped('name')
            msg = 'Bypassing the sending of autosubscribe mail regarding %s ' \
                  'IDs %s to partners %s' % (self._name,
                                             records,
                                             partners)
            _logger.debug(msg)
            return
        else:
            # If no bypass, fall back to core functionality
            return super(MailThread, self) \
                ._message_auto_subscribe_notify(partner_ids)
