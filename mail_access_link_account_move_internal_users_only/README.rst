.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================================
Mail: Access Link for Invoices for Internal Users Only
======================================================

* Hide the 'View invoice' link in emails from other recipients (customers, portal users etc)

Configuration
=============
* None needed

Usage
=====
* Send invoice via email. Message header no longer has the "View invoice button" if recipient
  is not an internal user

Known issues / Roadmap
======================
* Currently affects all types of account.move records (customer invoices, supplier invoices...),
  consider adding configurable options for each separately if needed.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
