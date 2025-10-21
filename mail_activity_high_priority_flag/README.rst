.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Activity: High Priority Flag
============================

* Enables flagging activities with a simple "High Priority"
  boolean
* Each Odoo object that inherits from the activity mixin
  (leads, tasks...) have a new stored field "Contains High 
  Priority Activities" that can be used for filtering 
  records.

Configuration
=============
* None needed

Usage
=====
* Create a new activity for a record, and check the 
  High Priority Box

Known issues / Roadmap
======================
* Meetings do not currently support the flag
* If you want the Contains High Priority Activities field
  to show up in the parent object's views, implement
  those in their own modules. See 
  mail_activity_high_priority_flag_crm_lead for a lead-based
  example.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
