# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cash_rounding_id = fields.Many2one('account.cash.rounding', string=u'抹零方式',
                                       readonly=True, states={'draft': [('readonly', False)]},)

    @api.onchange('order_line','cash_rounding_id')
    def _onchange_cash_rounding(self):
        lines_to_remove = self.order_line.filtered(lambda l: l.is_rounding_line)
        if lines_to_remove:
            self.order_line -= lines_to_remove

        if self.cash_rounding_id:
            rounding_amount = self.cash_rounding_id.compute_difference(self.currency_id, self.amount_total)
            if not self.currency_id.is_zero(rounding_amount):
                rounding_line = self.env['sale.order.line'].new({
                    'product_id':self.cash_rounding_id.product_id.id,
                    'name': self.cash_rounding_id.name,
                    'order_id': self.id,
                    'price_unit': rounding_amount,
                    'product_uom':self.cash_rounding_id.product_id.uom_id.id,
                    'product_uom_qty': 1,
                    'is_rounding_line': True,
                    'sequence': 9999  # always last line
                })

                if not rounding_line in self.order_line:
                    self.order_line += rounding_line


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_rounding_line=fields.Boolean(u'抹零行')

