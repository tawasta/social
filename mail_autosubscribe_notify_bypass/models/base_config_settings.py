# -*- coding: utf-8 -*-
from odoo import fields, models


class BaseConfigSettings(models.TransientModel):

    _inherit = 'base.config.settings'

    autosubscribe_bypass_model_ids = fields.Many2many(
        related='company_id.autosubscribe_bypass_model_ids',
        string='Autosubscribe Notification Bypass',
    )
