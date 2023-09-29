from odoo import models, fields, api
from .utils import console_log
import json


class Warehouse(models.Model):
    _name = 'stock.warehouse'
    pricelist = fields.Many2one('product.pricelist', string='Pricelist')

    
    @api.model
    def create(self, vals):
        # Create the warehouse record
        warehouse = super(Warehouse, self).create(vals)

        # Create a price list for the warehouse
        price_list = self.env['product.pricelist'].create({
            'name': "{} Pricelist".format(warehouse.name),
            # Add other price list fields as needed
        })

        # Link the price list to the warehouse
        warehouse.write({'pricelist': price_list.id})

        return warehouse
    
    @api.model
    def write(self, vals):
        # Create the warehouse record
        warehouse = super(Warehouse, self).write(vals)

        # Create a price list for the warehouse
        price_list = self.env['product.pricelist'].create({
            'name': "{} Pricelist".format(warehouse.name),
            # Add other price list fields as needed
        })

        # Link the price list to the warehouse
        warehouse.write({'pricelist': price_list.id})

        return warehouse

    

Warehouse()
