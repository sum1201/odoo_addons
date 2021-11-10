from odoo.addons.survey.controllers import main
from odoo.osv import expression
from odoo import http, _, fields
from odoo.http import request
import pytz
from dateutil.relativedelta import relativedelta


class Survey(main.Survey):

    def _get_user_input_domain(self, survey, line_filter_domain, **post):
        user_input_domain = super(Survey, self)._get_user_input_domain(survey, line_filter_domain, **post)
        if post.get('date_begin'):
            date = fields.Datetime.from_string(post.get('date_begin')) \
                .replace(tzinfo=pytz.timezone(request.env.user.tz)).astimezone(pytz.utc).replace(tzinfo=None)
            user_input_domain = expression.AND([[('create_date', '>=', date)], user_input_domain])
        if post.get('date_end'):
            date = (fields.Datetime.from_string(post.get('date_end')) + relativedelta(days=1)) \
                .replace(tzinfo=pytz.timezone(request.env.user.tz)).astimezone(pytz.utc).replace(tzinfo=None)
            user_input_domain = expression.AND([[('create_date', '<', date)], user_input_domain])
        return user_input_domain

    def _extract_filters_data(self, survey, post):
        user_input_lines, search_filters = super(Survey, self)._extract_filters_data(survey, post)
        if post.get('date_begin'):
            search_filters.append({
                'question': '调查起始日期',
                'answers': post.get('date_begin')
            })
        if post.get('date_end'):
            search_filters.append({
                'question': '调查截止日期',
                'answers': post.get('date_end')
            })
        return user_input_lines, search_filters


