.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================================
Combine purchase workorders and BoM attachment fetching
=======================================================

When a purchase order was created from work orders, the BoM attachments of the
purchase e-mail are fetched from the products of the work orders, that is the
manufactured products, instead of the order line products. The attachments of
their components and child BoMs are fetched recursively.

* A purchase order without work orders uses its order line products
* Other models selected for the recursive attachment search, for example a
  sales order, use their order line products
* Each manufactured product is searched once, also when the purchase was
  created from several work orders of the same manufacturing order
* Purchase users without manufacturing rights can send purchase orders: the
  work orders are read only to find their products

Configuration
=============
Nothing needs to be configured. The recursive BoM attachment search and the
creation of purchases from work orders are configured in the dependencies.

Usage
=====
* Create a purchase order from a work order
* Click Send by Email on the purchase order
* The attachments of the manufactured product and its BoM components are
  listed in the e-mail composer

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@tawasta.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
