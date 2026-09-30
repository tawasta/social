.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================================
Add attachment from order line product BoMs recursively
=======================================================

::

    List all the available attachments from product BoM components recursively.

    For example product A is on purchase and this product has a BoM:
    - Component A
    - Component B
    - Component C

    These components all have their own child BoMs which have their own
    attachments in their products. This module adds all those attachments
    to be selectable for the e-mail from purchase.

    Different models can be chosen to use this feature, meaning the same
    attachments can be fetched on sales. It is also possible to choose
    how far attachments are to be fetched from BoMs and their BoMs and
    so on.

Configuration
=============
::

    Go to General Settings to set models and recursive level for attachments fetching.

Usage
=====
::

    Open up an e-mail wizard for example from purchase to see how attachments are
    fetched to it.

Known issues / Roadmap
======================
::

    None known

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
