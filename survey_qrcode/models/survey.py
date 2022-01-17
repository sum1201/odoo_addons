from odoo import fields, models, api
import io, base64
import werkzeug
import logging
_logger = logging.getLogger(__name__)


class Survey(models.Model):
    _inherit = 'survey.survey'

    qrcode = fields.Binary('二维码', compute='_compute_qrcode')
    success_ratio_average = fields.Integer("平均分", compute="_compute_survey_statistic")

    @api.depends('access_token')
    def _compute_qrcode(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for survey_id in self:
            data = io.BytesIO()
            import qrcode
            survey_start_url = werkzeug.urls.url_join(base_url, survey_id.get_start_url()) if survey_id else False
            qrcode.make(survey_start_url, box_size=4).save(data, optimise=True, format='PNG')
            survey_id.qrcode = base64.b64encode(data.getvalue()).decode()

    @api.depends('user_input_ids.state', 'user_input_ids.test_entry', 'user_input_ids.scoring_percentage',
                 'user_input_ids.scoring_success')
    def _compute_survey_statistic(self):
        default_vals = {
            'answer_count': 0, 'answer_done_count': 0, 'success_count': 0,
            'answer_score_avg': 0.0, 'success_ratio': 0.0
        }
        stat = dict((cid, dict(default_vals, answer_score_avg_total=0.0)) for cid in self.ids)
        UserInput = self.env['survey.user_input']
        base_domain = ['&', ('survey_id', 'in', self.ids), ('test_entry', '!=', True), ('state', '=', 'done'), ]

        read_group_res = UserInput.read_group(base_domain, ['survey_id', 'state'],
                                              ['survey_id', 'state', 'scoring_percentage', 'scoring_success'],
                                              lazy=False)
        for item in read_group_res:
            stat[item['survey_id'][0]]['answer_count'] += item['__count']
            stat[item['survey_id'][0]]['answer_score_avg_total'] += item['scoring_percentage'] * item['__count']
            if item['state'] == 'done':
                stat[item['survey_id'][0]]['answer_done_count'] += item['__count']
            if item['scoring_success']:
                stat[item['survey_id'][0]]['success_count'] += item['__count']

        for survey_id, values in stat.items():
            avg_total = stat[survey_id].pop('answer_score_avg_total')
            stat[survey_id]['answer_score_avg'] = avg_total / (stat[survey_id]['answer_done_count'] or 1)
            stat[survey_id]['success_ratio'] = (stat[survey_id]['success_count'] / (
                        stat[survey_id]['answer_done_count'] or 1.0)) * 100

        for survey in self:
            survey.update(stat.get(survey._origin.id, default_vals))

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


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    @api.depends('scoring_percentage', 'survey_id.scoring_success_min')
    def _compute_scoring_success(self):
        for user_input in self:
            user_input.scoring_success = user_input.scoring_percentage >= user_input.survey_id.scoring_success_min