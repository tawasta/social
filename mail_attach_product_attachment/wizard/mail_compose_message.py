# -*- coding: utf-8 -*-
from odoo import models, api


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def _compute_object_attachment_ids(self):
        # This would set all attachments as selected
        res_id = self.env.context.get('active_id')
        model = self.env.context.get('active_model')

        IrAttachment = self.env['ir.attachment']

        attachment_ids = IrAttachment.search([
            ('res_model', '=', model),
            ('res_id', '=', res_id)
        ])

        # If model is SO or PO, include their line product attachments
        if model in ['sale.order', 'purchase.order']:
            OrderObject = self.env[model]
            order = OrderObject.browse([res_id])

            product_ids = [line.product_id.id for line in order.order_line]

            # Product attachments
            product_attachment_ids = IrAttachment.search([
                ('res_model', '=', 'product.product'),
                ('res_id', 'in', product_ids),
            ])
            attachment_ids += product_attachment_ids

            # Product template attachments
            template_ids = product_ids.mapped('product_tmpl_id')
            template_attachment_ids = IrAttachment.search([
                ('res_model', '=', 'product.template'),
                ('res_id', 'in', template_ids),
            ])
            attachment_ids += template_attachment_ids

        return attachment_ids

    # Uncomment to select all attachments as default.
    # This should be implemented as configurable, if necessary

    # object_attachment_ids = fields.Many2many(
    #     default=_compute_object_attachment_ids,
    # )

    @api.model
    def _get_object_attachment_domain(self):
        domain = super(MailComposeMessage,
                       self)._get_object_attachment_domain()

        context = self.env.context
        model = context.get('active_model')

        # Add line product attachments if model is SO or PO
        if model in ['sale.order', 'purchase.order']:
            res_id = context.get('active_id')

            order = self.env[model].browse([res_id])
            product_ids = [line.product_id.id for line in order.order_line]
            template_ids = [line.product_id.product_tmpl_id.id
                            for line in order.order_line]

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
