odoo.define('sale_barcode.SaleOrderBarcodeHandler', function (require) {
    "use strict";

    var field_registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var FormController = require('web.FormController');

    FormController.include({
        _barcodeSaleAddRecordId: function (barcode, activeBarcode) {
            if (!activeBarcode.handle) {
                return $.Deferred().reject();
            }
            var record = this.model.get(activeBarcode.handle);
            if (record.data.state != 'draft') {
                this.do_warn("销售订单", '只能对草稿状态的单据增加明细');
                return $.Deferred().reject();
            }
            return this._barcodeAddX2MQuantity(barcode, activeBarcode);
        }
    })

    var SaleOrderBarcodeHandler = AbstractField.extend({
        init: function () {
            this._super.apply(this, arguments);

            this.trigger_up('activeBarcode', {
                name: this.name,
                fieldName: 'order_line',
                quantity: 'product_qty',
                setQuantityWithKeypress: true,
                commands: {
                    // 'O-CMD.MAIN-MENU': _.bind(this.do_action, this, 'stock_barcode.stock_barcode_action_main_menu', {clear_breadcrumbs: true}),
                    barcode: '_barcodeSaleAddRecordId',
                }
            });
        },
    });

    field_registry.add('saleorder_barcode_handler', SaleOrderBarcodeHandler);

});
