from odoo import fields, models


class IrAttachmentFileType(models.TransientModel):
    _name = "ir.attachment.file.type"
    _description = "Attachment File Type"

    name = fields.Char()
    file_type = fields.Char()
    is_filter = fields.Boolean(default=True)
    active = fields.Boolean(default=True)
