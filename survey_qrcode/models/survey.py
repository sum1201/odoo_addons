from odoo import fields, models, api
import io, base64
import werkzeug
import logging
_logger = logging.getLogger(__name__)


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

    def _prepare_statistics(self, user_input_lines=None):
        result = super(Survey, self)._prepare_statistics(user_input_lines)
        if user_input_lines:
            user_input_domain = [
                ('survey_id', 'in', self.ids),
                ('id', 'in', user_input_lines.mapped('user_input_id').ids)
            ]
        else:
            user_input_domain = [
                ('survey_id', 'in', self.ids),
                ('state', '=', 'done'),
                ('test_entry', '=', False)
            ]
        scoring_data = self.env['survey.user_input'].sudo().read_group(
            user_input_domain, ['scoring_percentage'], ['scoring_percentage'])
        scoring_total = 0
        scoring_count = 0
        for scoring_data_item in scoring_data:
            scoring_total += scoring_data_item['scoring_percentage'] * scoring_data_item['scoring_percentage_count']
            scoring_count += scoring_data_item['scoring_percentage_count']
        if scoring_data:
            _logger.info(scoring_total)
            _logger.info(scoring_data)
            global_scoring_percentage = round(scoring_total / scoring_count, 2)
        else:
            global_scoring_percentage = 0.0
        result.update({'global_scoring_percentage': global_scoring_percentage})
        return result

    def action_result_survey(self):
        self.ensure_one()
        return {
            'name': '调查结果向导',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'survey.result.wizard',
            'target': 'new',
        }
        return action
