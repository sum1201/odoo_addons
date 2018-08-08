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
    "name": "Sale Add Product By Scan",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base", "barcodes", "sale"],
    "author": "山西清水欧度信息技术有限公司",
    "category": "Sales",
    'website': 'http://www.odooqs.com',
    "description": """
        Scan directly using scan code equipment 
    """,
    "data": [
        'views/sale_barcode_template.xml',
        'views/sale_order_view.xml',
    ],
    "init_xml": [],
    'update_xml': [],
    'demo_xml': [],
    'images': ['static/description/barcode_01.jpg','static/description/main_screenshot.png'],
    'installable': True,
    'active': False,
    #    'certificate': '',
}
