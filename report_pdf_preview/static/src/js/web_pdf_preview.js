odoo.define('report_pdf_preview.report', function (require) {
    'use strict';

    const ActionManager = require('web.ActionManager');
    const { qweb} = require('web.core');
    const Dialog = require('web.Dialog');

    ActionManager.include({
        _executeReportAction: function (action, options) {
            const self = this;
            action = _.clone(action);

            if (action.report_type === 'qweb-pdf') {
                return this.call('report', 'checkWkhtmltopdf').then(function (state) {
                    const url = `/web/static/lib/pdfjs/web/viewer.html?file=${self._makeReportUrls(action).pdf}`

                    const dialog = new Dialog(this, {
                        title: action.name,
                        size: 'large',
                        $content: $(qweb.render('report_pdf_preview.ReportViewer', {url: url})),
                    });
                    dialog.open();
                });

            } else {
                return self._super(action, options);
            }

        }
    });

});