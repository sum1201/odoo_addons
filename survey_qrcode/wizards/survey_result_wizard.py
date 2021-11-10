from odoo import fields, models, api


class SurveyResultWizard(models.TransientModel):
    _name = 'survey.result.wizard'
    _description = '调查结果查看向导'

    type = fields.Selection([('all', '所有'), ('manual', '指定')], '类型', default='all', required=True)
    date_begin = fields.Date('开始日期')
    date_end = fields.Date('结束日期')

    def button_done(self):
        self.ensure_one()
        if self.type == 'manual':
            url = '/survey/results/%s?date_begin=%s&date_end=%s' % (self.env.context.get('active_id'),
                                                                    self.date_begin, self.date_end)
        else:
            url = '/survey/results/%s' % self.env.context.get('active_id')
        return {
            'type': 'ir.actions.act_url',
            'name': "Results of the Survey",
            'target': 'self',
            'url': url
        }