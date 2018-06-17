# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import odoo.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_barcode = fields.Char(related='product_id.barcode')


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    def _add_product(self, product, qty=1.0):
        order_line = self.order_line.filtered(lambda r: r.product_id.id == product.id)
        if order_line:
            order_line.product_qty = qty
        else:
            product_lang = product.with_context({
                'lang': self.partner_id.lang,
                'partner_id': self.partner_id.id,
            })
            name = product_lang.display_name
            if product_lang.description_purchase:
                name += '\n' + product_lang.description_purchase

            vals = {
                'product_id': product.id,
                'name': name,
                'product_uom': product.uom_id.id,
                'product_uom_qty': 1,
                'price_unit': product.lst_price,
                'state': 'draft',
            }
            new_order_line = self.order_line.new(vals)
            self.order_line += new_order_line
            new_order_line.product_id_change()
            new_order_line.product_uom_change()
            new_order_line._onchange_discount()

    def on_barcode_scanned(self, barcode):
        product = self.env['product.product'].search(['|', ('barcode', '=', barcode), ('default_code', '=', barcode)])
        if product:
            self._add_product(product)
