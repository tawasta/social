.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================================
Mail: Amount of Purchase order is always hidden
===============================================

Some installations do not want that the total amount is shown
in purchase order's mails. This module hides this amount in mails.

Configuration
=============
None needed

Usage
=====
Installing this module is only needed

Known issues / Roadmap
======================
In case an amount is still shown, maybe check if an other module inherits
_notify_by_email_prepare_rendering_context method of purchase.order.

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
