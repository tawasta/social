from odoo import fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    email_product_clause_ids = fields.Many2many(
        comodel_name="email.product.clause",
        string="E-mail Product Clauses",
    )
