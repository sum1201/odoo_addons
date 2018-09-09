# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_default_cash_rounding_id(self):
        round_ids=self.env['account.cash.rounding'].search([],limit=1)
        if round_ids:
            return round_ids[0]

    cash_rounding_id = fields.Many2one('account.cash.rounding', string=u'抹零方式',default=_get_default_cash_rounding_id,
                                       readonly=True, states={'draft': [('readonly', False)]},)
    auto_cash_round=fields.Boolean(u'自动抹零',default=True,readonly=True, states={'draft': [('readonly', False)]},)

    @api.onchange('order_line','cash_rounding_id','auto_cash_round')
    def _onchange_cash_rounding(self):
        if self.auto_cash_round:
            self._cash_rounding()

    @api.multi
    def button_cash_round(self):
        self._cash_rounding()

    def _cash_rounding(self):
        lines_to_remove = self.order_line.filtered(lambda l: l.is_rounding_line)
        if lines_to_remove:
            self.order_line -= lines_to_remove

        if self.cash_rounding_id and self.order_line:
            rounding_amount = self.cash_rounding_id.compute_difference(self.currency_id, self.amount_total)
            if not self.currency_id.is_zero(rounding_amount):
                rounding_line = self.env['sale.order.line'].new({
                    'product_id': self.cash_rounding_id.product_id.id,
                    'name': self.cash_rounding_id.name,
                    'order_id': self.id,
                    'price_unit': rounding_amount,
                    'product_uom': self.cash_rounding_id.product_id.uom_id.id,
                    'product_uom_qty': 1,
                    'is_rounding_line': True,
                    'sequence': 9999  # always last line
                })

                if not rounding_line in self.order_line:
                    self.order_line += rounding_line

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_rounding_line=fields.Boolean(u'抹零行')

