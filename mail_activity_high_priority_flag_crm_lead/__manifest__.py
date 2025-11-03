##############################################################################
#
#    Author: Futural Oy
#    Copyright 2025 Futural Oy (https://futural.fi)
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
    "name": "Activity: High Priority Flag - Show Column in Lead Views",
    "summary": "Show the 'Contains High Priority Activities' field in " "lead views",
    "category": "Social",
    "version": "17.0.1.0.0",
    "website": "https://github.com/tawasta/social",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": False,
    "depends": ["mail_activity_high_priority_flag", "crm"],
    "data": ["views/crm_lead.xml"],
}
