# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import odoo.addons.decimal_precision as dp


class StockPackOperation(models.Model):
    _inherit = 'stock.pack.operation'

    gross_weight = fields.Float(u'Gross Weight')
    tare_weight = fields.Float(u'Tare_weight')
