##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2024 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    "name": "Mass Mailing: base_fontawesome Compatible Icons",
    "summary": "Replaces mass mailing's social media icon classes to work with OCA's module",
    "version": "14.0.1.0.0",
    "category": "Tools",
    "website": "https://gitlab.com/tawasta/odoo/social",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base_fontawesome",
        "mass_mailing",
        "mass_mailing_social_links_youtube",
    ],
    "data": [
        "views/snippets_theme.xml",
    ],
}
