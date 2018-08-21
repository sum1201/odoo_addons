# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import odoo.addons.decimal_precision as dp


class AccountCashRounding(models.Model):
    _inherit = 'account.cash.rounding'

    product_id=fields.Many2one('product.product',u'产品',required=True)