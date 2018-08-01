from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import odoo.addons.decimal_precision as dp


class ResUsers(models.Model):
    _inherit = 'res.users'

    scale = fields.Many2one('scale.info', 'Scale')
