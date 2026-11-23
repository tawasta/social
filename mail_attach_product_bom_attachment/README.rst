.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================================
Add attachment from order line product BoMs recursively
=======================================================

Lists the attachments of the order line products and of their BoM components
recursively, so that they can be selected for the e-mail of the order.

For example product A is on a purchase and it has a BoM with components A, B
and C. The components have their own child BoMs, and their products have
attachments. All those attachments can be selected for the e-mail of the
purchase.

* The attachments can be filtered by file type, and each attachment can be
  selected or left out of the e-mail
* An attachment that is on several products is listed once
* A warning is shown and the Send button is hidden when the selected
  attachments are larger than the size limit
* For a product variant, only the BoMs of that variant and the BoMs shared by
  all variants of the product are used
* An attachment that is on a mail message is not deleted: it is only removed
  from the messages, so that the product keeps its own file
* Users who cannot edit products, for example purchase users, can send the
  attachments

Configuration
=============
* Go to Settings > General Settings > Recursive attachment search
* Select the models that fetch the attachments, for example Purchase Order
* Set the recursive level, that is how many child BoM levels are searched
* Set the size limit of the selected attachments in bytes (0 = no limit)
* The system parameter attachment_file_type_list, for example
  [("pdf", "PDF")], gives the options of the attachment_file_type field. It is
  not needed in 19.0, see Intended behaviour

Usage
=====
* Open the e-mail composer, for example Send by Email on a purchase order
* Select the file types and the attachments to send

Intended behaviour
==================
The following behaviour is intentional. It was reviewed in the 19.0 migration
and must be kept in later migrations:

* The e-mail composer has the selection field attachment_file_type with the
  default value "all", and its options come from the system parameter
  attachment_file_type_list. The field is kept as it is. In 17.0, without the
  parameter, sending an e-mail from the composer and installing or updating
  the module failed with "Wrong value for
  mail.compose.message.attachment_file_type: 'all'". The 19.0 core does not
  validate a selection whose options come from a function, so in 19.0 e-mails
  can be sent without the parameter
* Deleting an attachment that is on a mail message does not delete it: the
  attachment is only removed from the messages. The e-mail uses the product's
  own attachment, so deleting it from a sent message must not delete the
  product's file. This applies to every attachment, also when it is deleted
  from the product or from the attachment list, and the sent message then no
  longer shows it
* The recursive level grows with every component that has a child BoM, also
  between components of the same BoM. Child BoMs of later components may
  therefore be left out. This limits the number of extra attachments

Changes in 19.0
===============
* The Send button stays hidden on log notes. In 17.0 the size limit condition
  replaced the core condition, so a log note showed both Send and Log
* The size limit also hides the Schedule button, which is new in 19.0
* The BoM attachment section is hidden in mass mailing, as in 17.0
* The BoMs of other variants are no longer used. In 17.0 the attachments of
  the BoMs of all variants were listed for a variant, and a variant used as a
  BoM component used the first BoM of the product instead of its own BoM

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
