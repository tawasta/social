from odoo import api, models


class Contract(models.Model):

    _inherit = "contract.contract"

    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, *args, **kwargs):
        res = super().message_post(
            *args,
            **kwargs,
        )

        res._mail_message_auto_activity(self)

        return res
