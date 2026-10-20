.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================
Email Marketing: Limited Sender Group
=====================================

* Adds a new group "Email Marketing: Limited Sender". Users in it can edit, test,
  schedule and send mass mailings, but they cannot create mailings or change who
  receives them. An Email Marketing user creates the mailing and sets its
  recipients.
* The restriction is mainly done in the user interface. It is not meant to stop a
  determined user from reading list or statistics data through other means.

Configuration
=============

* Give users the "Email Marketing: Limited Sender" right (Extra Rights section of
  the user form), but do not give them the core "Email Marketing: User" right.

Usage
=====
* A person with core "Email Marketing: User" rights creates the mailing and 
  sets its recipients first.
* The limited sender then opens it in Email Marketing > Mailings, edits the content
  and tests, schedules or sends it.

Known issues / Roadmap
======================
* Note that when a limited sender sends a mailing, dynamic mailing lists from
  ``mass_mailing_list_dynamic`` get synced with sudo() instead of trying with 
  the user's insufficient rights.

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
