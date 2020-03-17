from odoo import api
from odoo import fields
from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def _get_object_attachment_domain(self):
        context = self.env.context
        model = context.get('default_model')
        domain = False

        # Add line product attachments if model is SO or PO
        if model in ['sale.order', 'purchase.order']:
            res_id = context.get('default_res_id')

            order = self.env[model].browse([res_id])
            product_ids = order.order_line.mapped('product_id.id')
            template_ids = order.order_line.mapped(
                'product_id.product_tmpl_id.id')

            # (model = res_model AND id = res_id) OR
            # (model = product.product AND id in product_ids) OR
            # (model = product.template AND id in template_ids)
            domain = [
                '|', '|',
                '&',
                ('res_model', '=', model),
                ('res_id', '=', res_id),
                '&',
                ('res_model', '=', 'product.product'),
                ('res_id', 'in', product_ids),
                '&',
                ('res_model', '=', 'product.template'),
                ('res_id', 'in', template_ids),
            ]

        return domain

    object_attachment_ids = fields.Many2many(
        domain=lambda self: self._get_object_attachment_domain()
    )
