.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================================================
Enable to Log note in chatter even with readonly access rights
==============================================================

::

    A user might only have readonly access rights to a certain model.
    This prevent the user from adding notes to chatter. Installing
    this module will override this restriction and a user can send
    notes any model even if the user has only readonly access to the model
    to which the note is added to.

Configuration
=============
::

    There is no need to configure anything.

Usage
=====
::

    Go to a model, for example partner form view if contacts are enabled.
    Then write a note in the chatter of the form view. This is possible
    even if a user would have only readonly access rights to the model.

Known issues / Roadmap
======================
::

    Check if adding notes should be restricted on some models. Then consider
    expanding this module to use optional models in the settings.

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
