# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import odoo.addons.decimal_precision as dp

class ScaleInfo(models.Model):
    _name = 'scale.info'
    _description = u'Scale Info'
    _order="sequence,id"

    sequence=fields.Integer(u'Sequence',default=10)
    name=fields.Char(u'Name',required=True)
    ip_address =fields.Char(u'IP Address',required=True)





