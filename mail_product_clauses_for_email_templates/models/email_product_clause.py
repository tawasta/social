from odoo import fields, models


class EmailProductClause(models.Model):

    _name = "email.product.clause"
    _description = "E-mail Product Clause"
    _order = "sequence, name"

    # Currently limited to models that support preview on their form view.
    _model_domain = [("model", "in", ["sale.order", "account.move"])]

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence")

    clause_contents = fields.Html(string="Clause Contents", translate=True)

    ir_model_ids = fields.Many2many(
        comodel_name="ir.model",
        domain=_model_domain,
        string="Apply to Models",
        required=True,
    )

    product_template_ids = fields.Many2many(
        comodel_name="product.template",
        string="Product Templates Applied To",
        help="The clause will be appended to the e-mail if these "
        "products are a part of the parent record, e.g. invoice",
    )

    product_category_ids = fields.Many2many(
        comodel_name="product.category",
        string="Product Categories Applied To",
        help="The clause will be appended to the e-mail if these products "
        "belonging to these categories are a part of the parent record, e.g. invoice",
    )

    internal_notes = fields.Text(string="Internal Notes")
