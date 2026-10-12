.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================================
Combine purchase workorders and BoM attachment fetching
=======================================================

::

    Enable to get attachments from products of manufacturing orders of work orders
    of purchase orders. Maybe in simpler terms this means that the related manufacturing
    product attachments recursively from its components and their child BoMs are fetched
    for the e-mail to be sent from Purchase Order.

Configuration
=============
::

    Nothing is required to be configured. But see how the dependencies,
    mail_attach_product_bom_attachment and mrp_create_purchase_from_work_order,
    of this module work.

Usage
=====
::

    Send an e-mail from purchase order with related work orders
    to test the functionality.

Known issues / Roadmap
======================
::

    The module directly modifies get_product_bom_attachments function.

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
