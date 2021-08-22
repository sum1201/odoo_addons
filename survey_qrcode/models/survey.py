from odoo import fields, models, api
import io, base64


class Survey(models.Model):
    _inherit = 'survey.survey'

    qrcode = fields.Binary('二维码', compute='_compute_session_link')

    @api.depends('session_code')
    def _compute_session_link(self):
        super(Survey, self)._compute_session_link()
        for survey in self:
            data = io.BytesIO()
            import qrcode
            qrcode.make(survey.session_link, box_size=4).save(data, optimise=True, format='PNG')
            survey.qrcode = base64.b64encode(data.getvalue()).decode()