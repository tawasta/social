.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================
Mail: Access Link for Purchase Orders always Hidden
===================================================

* Hide the access link in emails from all recipients, regardless if they're an internal user,
  supplier etc

Configuration
=============
* None needed

Usage
=====
* Send PO via email. Message header no longer has the access link button
  or the linked document name

Known issues / Roadmap
======================
* New in Odoo 19: the standard purchase order and vendor reminder e-mail
  templates contain an "Acknowledge" button in the message body (in Odoo 17
  the templates had no link). The button links to the order in the portal
  with an access token and is not hidden by this module. Remove it from the
  e-mail templates if vendors must not get portal access

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy.
