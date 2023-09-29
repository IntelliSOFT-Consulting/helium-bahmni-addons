from odoo import models, fields, api, _
from .utils import console_log
from odoo.exceptions import UserError
import datetime


class Pricelist(models.Model):

    _inherit = 'product.pricelist'
    warehouse = fields.Many2one('stock.warehouse', string='Warehouse', unique=True)

Pricelist()