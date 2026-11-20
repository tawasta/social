##############################################################################
#
#    Author: Futural Oy
#    Copyright 2026- Futural Oy (https://futural.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

{
    "name": "Mail compose attachment preview",
    "summary": "Enable previewing mail composing attachments in browser",
    "category": "Social",
    "version": "19.0.1.0.0",
    "website": "https://github.com/tawasta/social",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mail",
    ],
    "assets": {
        "web.assets_backend": [
            "mail_compose_attachment_preview/static/src/js/mail_composer_attachment_list.esm.js",
            "mail_compose_attachment_preview/static/src/xml/mail_composer_attachment_list.xml",
        ],
    },
}
