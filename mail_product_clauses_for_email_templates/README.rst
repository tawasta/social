.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================
Mail: Product Clauses for E-mail Templates
==========================================

* Enables configuring messages for products/categories that can then be appended to emails
  such as order confirmations and invoices.
* Intended for situations where you want to e.g. inform the buyer in order confirmation
  how they can access their bought online courses, but you want to show that information
  message only if they actually bought courses, not when they bought just e.g. physical products


Configuration
=============
* Create the clauses via Settings -> Technical -> E-mail Product Clauses (sales manager rights required):

  * You can apply a clause to product templates or entire categories of products.

    * Note: only clauses of the direct parent category will be shown, not those of a
      multilevel category hierarchy's ancestor categories.

  * Set if the clause is related to sale orders or invoices, or both
  * Type in the clause contents and translate them as necessary. Note: you can use 
    ${o.fieldname} notation to access the fields of parent Sale Order or Invoice, if needed.
  * Finally, set the clauses' preferred order in the treeview with the sequence handle

Usage
=====
* In your Sale Order or Invoice email template of choice, apply ${object.email_product_clause_contents|safe}.
* Hit preview, and the rendered clauses will show up.
* Additionally, you can go to Sale Order or Invoice form view, and you can 
  see in the notebook what clauses will be applied to that particular SO/Invoice.

Known issues / Roadmap
======================
* Add support for other object types as needed
* Add access also to product and category records with ${} notation
* Add configurable separator between rendered clauses (currently BR tag)

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
