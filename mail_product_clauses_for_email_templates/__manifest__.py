##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2024 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

{
    "name": "Mail: Product Clauses for E-mail Templates",
    "summary": "Configure messages for products/categories that can then be appended to mails",
    "version": "14.0.1.0.0",
    "category": "Social",
    "website": "https://gitlab.com/tawasta/odoo/social",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["mail", "sale"],
    "data": [
        "security/ir_model_access.xml",
        "views/email_product_clause.xml",
        "views/account_move.xml",
        "views/sale_order.xml",
        "views/product_category.xml",
        "views/product_template.xml",
    ],
}
