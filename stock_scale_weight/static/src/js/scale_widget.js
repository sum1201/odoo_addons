odoo.define('stock_scale_weight.scale_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.DataModel');
    var session = require('web.session');
    var common = require('web.form_common');
    var devices = require('stock_scale_weight.scale_device');
    var form_widget = require('web.form_widgets');

    var QWeb = core.qweb;
    var _t = core._t;

    var WidgetScale = form_widget.FieldFloat.extend({
        template:"FieldScale",
        start: function () {
            var self = this;
            var tmp = this._super();
            var proxy = new devices.ProxyDevice(this);
            var queue = new devices.JobQueue();
            $.when(self, proxy, queue, proxy.autoconnect({
                force_ip: session.scale_ip_address || undefined,
            })).then(function (self, proxy, queue) {
                queue.schedule(function () {
                    return proxy.scale_read().then(function (weight) {
                        self.set_value(weight.weight);
                    });
                }, {duration: 150, repeat: true});

            })
            return tmp;
        },
    })
    core.form_widget_registry.add('scale', WidgetScale);
})