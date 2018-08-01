# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import odoo.addons.decimal_precision as dp


class ResConfigSettings(models.TransientModel):
    _inherit = "base.config.settings"

    dingtalk_app_id=fields.Char(u'钉钉appid')
    dingtalk_qr_appSecret=fields.Char(u'钉钉扫码appSecret')
    dingtalk_corpid = fields.Char(u'钉钉应用corpid')
    dingtalk_corpSecret=fields.Char(u'钉钉应用corpSecret')

    @api.multi
    def set_dingtalk_app_id(self):
        self.env['ir.config_parameter'].set_param('dingtalk.appid', self[0].dingtalk_app_id)

    @api.multi
    def set_dingtalk_qr_appSecret(self):
        self.env['ir.config_parameter'].set_param('dingtalk.qr.appsecret', self[0].dingtalk_qr_appSecret)

    @api.multi
    def set_dingtalk_corpid(self):
        self.env['ir.config_parameter'].set_param('dingtalk.corpid', self[0].dingtalk_corpid)

    @api.multi
    def set_dingtalk_corpSecret(self):
        self.env['ir.config_parameter'].set_param('dingtalk.corpSecret', self[0].dingtalk_corpSecret)

    @api.multi
    def get_default_dingtalk_app_id(self, fields):
        params = self.env['ir.config_parameter']
        appid = params.get_param('dingtalk.appid', default='')
        return {'dingtalk_app_id': appid}

    @api.multi
    def get_default_dingtalk_qr_appSecret(self, fields):
        params = self.env['ir.config_parameter']
        appsecret = params.get_param('dingtalk.qr.appsecret', default='')
        return {'dingtalk_qr_appSecret': appsecret}

    @api.multi
    def get_default_dingtalk_corpid(self, fields):
        params = self.env['ir.config_parameter']
        corpid = params.get_param('dingtalk.corpid', default='')
        return {'dingtalk_corpid': corpid}

    @api.multi
    def get_default_dingtalk_corpSecret(self, fields):
        params = self.env['ir.config_parameter']
        corpSecret = params.get_param('dingtalk.corpSecret', default='')
        return {'dingtalk_corpSecret': corpSecret}
