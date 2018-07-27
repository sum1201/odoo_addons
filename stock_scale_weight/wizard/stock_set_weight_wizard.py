# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import odoo.addons.decimal_precision as dp


class StockWeightWizard(models.TransientModel):
    _name = 'stock.weight.wizard'
    _description = u'Stock Set Weight Wizard'

    type = fields.Selection([('gross_weight', u'Gross Weight'), ('tare_weight', u'Tare Weight')], u'Type',
                            default='gross_weight')
    weight = fields.Float(u'Weight')

    @api.multi
    def button_set_weight(self):
        self.ensure_one()
        operation_id = self.env['stock.pack.operation'].browse(self.env.context.get('active_id', False))
        operation_id.write({self.type: self.weight, })
        operation_id.write({'qty_done': operation_id.gross_weight - operation_id.tare_weight})
