##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2024- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    "name": "Mass Mailing: Youtube in Social Media Icons",
    "summary": "Adds Youtube icon support to mass mailing blocks",
    "version": "17.0.1.0.0",
    "category": "Mass Mailing",
    "website": "https://github.com/tawasta/social",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["mass_mailing", "website_mass_mailing"],
    "data": [
        "views/snippets_theme.xml",
    ],
}
