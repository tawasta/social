.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Bypass Autosubscribe Notifications
==================================

* Adds a configuration option to set which models do not trigger the sending of
  the "You have been assigned..." autosubscribe notifications
* When a bypass occurred, a debug message is written to server log.

Configuration
=============
* Set the models whose notifications should be bypassed from
  Settings -> General Settings

Usage
=====
\-

Known issues / Roadmap
======================
* When fetching the list of models to bypass, the current company is checked
  from current user instead of the company of the record currently being
  handled. This is because all models may not have the company_id field
  available. As a result, in multicompany environments the bypassed model list
  is not company-specific, but should instead be configured to be identical
  for all companies in the system.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@tawasta.fi>
* Miika Nissi <miika.nissi@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
