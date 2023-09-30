from odoo import models, fields, api, _
from .utils import console_log
from odoo.exceptions import UserError
import datetime


class TenantUser(models.Model):

    _name = 'res.users'
    _inherit = 'res.users'

    x_warehouse = fields.Many2many("stock.warehouse")


TenantUser()