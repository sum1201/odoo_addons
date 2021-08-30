from odoo import fields, models, api
import io, base64
import werkzeug


class Survey(models.Model):
    _inherit = 'survey.survey'

    qrcode = fields.Binary('二维码', compute='_compute_qrcode')

    @api.depends('access_token')
    def _compute_qrcode(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for survey_id in self:
            data = io.BytesIO()
            import qrcode
            survey_start_url = werkzeug.urls.url_join(base_url, survey_id.get_start_url()) if survey_id else False
            qrcode.make(survey_start_url, box_size=4).save(data, optimise=True, format='PNG')
            survey_id.qrcode = base64.b64encode(data.getvalue()).decode()