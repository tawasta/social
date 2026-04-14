from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    website_id = fields.Many2one(comodel_name="website", string="Website")

    @api.model_create_multi
    def create(self, values):
        mailing = super(MassMailing, self).create(values)
        if not mailing.website_id:
            if mailing.create_uid and mailing.create_uid.website_id:
                mailing.website_id = mailing.create_uid.website_id
            elif mailing.create_uid and mailing.create_uid.company_id and mailing.create_uid.company_id.website_id:
                mailing.website_id = mailing.create_uid.company_id.website_id

        return mailing

