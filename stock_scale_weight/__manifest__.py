# -*- encoding: utf-8 -*-
#                                                                            #
#   OpenERP Module                                                           #
#   Copyright (C) 2013 Author <email@email.fr>                               #
#                                                                            #
#   This program is free software: you can redistribute it and/or modify     #
#   it under the terms of the GNU Affero General Public License as           #
#   published by the Free Software Foundation, either version 3 of the       #
#   License, or (at your option) any later version.                          #
#                                                                            #
#   This program is distributed in the hope that it will be useful,          #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#   GNU Affero General Public License for more details.                      #
#                                                                            #
#   You should have received a copy of the GNU Affero General Public License #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                            #

{
    "name": "Stock Product Scale Weight",
    "version": "10.0",
    "depends": ["base", "stock"],
    "author": "山西清水欧度信息技术有限公司",
    'website': 'http://www.odooqs.com',
    "category": "stock",
    "description": """
        Stock Product Scale Weight
    """,
    "data": [
        'wizard/stock_set_weight_wizard_view.xml',
        'views/scale_info_view.xml',
        "views/stock_view.xml",
        'views/res_users_view.xml',

        'views/template.xml',
        'security/ir.model.access.csv'
    ],
    "init_xml": [],
    'update_xml': [],
    'demo_xml': [],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'active': False,
    #    'certificate': '',
}
