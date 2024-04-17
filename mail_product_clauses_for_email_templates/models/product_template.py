from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    email_product_clause_ids = fields.Many2many(
        comodel_name="email.product.clause",
        string="E-mail Product Clauses",
    )
