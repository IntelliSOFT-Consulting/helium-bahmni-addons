from odoo import models, fields, api, _
from .utils import console_log
from odoo.exceptions import UserError
import datetime


class SaleOrder(models.Model):

    _name = 'sale.order'
    _inherit = 'sale.order'
         

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        if True:
            data = {}
            for attribute in self.partner_id.attribute_ids:
                data[attribute.name] = attribute.value
            console_log(data)
            if 'facilityName' in data:
                warehouse = self.env['stock.warehouse'].search(
                    [("name", "=", data['facilityName'])], limit=1)
                if not warehouse:
                    UserError("Facility information not found.")
                    return
                self.warehouse_id = warehouse[0]

                self.location_id = self.stock_location
                self.facility = self.warehouse_id
                self.write({'facility': self.facility})
                self.pricelist_id = self.warehouse_id.pricelist
        res = super(SaleOrder, self).fields_view_get(
        view_id=view_id, view_type=view_type, toolbar=toolbar,submenu=submenu)
        console_log("onLoad")
        console_log(res)
        console_log(self.partner_id)
        console_log(self)
        
        return res

    shop_id = fields.Many2one('sale.shop', string="Shop", default=lambda self: self.env['sale.shop'].search([], limit=1))
    facility = fields.Many2one('stock.warehouse', required=True)
    facility_name = fields.Char()
    stock_location  = fields.Many2one('stock.location', string="Dispensing Location", required=True)

    @api.onchange('facility')
    def _onchange_facility(self):
        if self.facility:
            self.warehouse_id = self.facility
            self.pricelist_id = self.warehouse_id.pricelist[0]
            self.facility_name = self.warehouse_id.name
            return

    @api.onchange('partner_id')
    def _onchange_customer(self):
        if self.partner_id:
            data = {}
            for attribute in self.partner_id.attribute_ids:
                data[attribute.name] = attribute.value
            console_log(data)
            if 'facilityName' in data:
                warehouse = self.env['stock.warehouse'].search(
                    [("name", "=", data['facilityName'])], limit=1)
                if not warehouse:
                    UserError("Selected facility information not found or invalid.")
                    return
                self.warehouse_id = warehouse[0]
                self.facility = warehouse[0]                
                # self.write({
                #     "warehouse_id":warehouse[0],
                #     "pricelist_id": self.warehouse_id.pricelist,
                #     "facility":self.warehouse_id
                # })
            return

    @api.model
    def update_warehouse_and_location(self):
        # if SaleOrder is not paid
        if not self.facility:
            UserError("Dispensing location is required.")
            return
        console_log("State: {}".format(self.state))
        if self.state == "draft":
            data = {}
            for attribute in self.partner_id.attribute_ids:
                data[attribute.name] = attribute.value
            # console_log(("insurance patient attributes: ", data))
            insurance_total = 0.0
            cash_total = 0.0
            if not 'facilityName' in data: # add location logic
                UserError("Facility information not found.")
                return
            
            facility_name = data['facilityName']
            console_log(facility_name)

            warehouse = self.env['stock.warehouse'].search(
                [("name", "=", data['facilityName'])], limit=1)
            if not warehouse:
                UserError("Facility information not found.")
                return
            self.facility = warehouse[0]
            # self.location_id = self.warehouse_id.lot_stock_id
            self.pricelist_id = self.warehouse_id.pricelist


            # with the new vals, amend the sale order 
            order_line = self.order_line

            for item in order_line:
                price = self.pricelist_id.get_product_price(
                    item.product_id, item.product_uom_qty, False)
                if price:
                    # console_log(price)
                    order_line_vals = {
                        'order_id': self.id,
                        'product_id': item.product_id.id,
                        'product_uom_qty': item.product_uom_qty,
                        'price_unit': price,
                    }
                    insurance_total += price * item.product_uom_qty
                    item.unlink()
                    self.env['sale.order.line'].create(order_line_vals)
                else:
                    cash_total += item.price_unit * item.product_uom_qty
            self.action_confirm()
            return
        self.action_confirm()
        return
    
    # @api.multi
    # def write(self, vals):
    #     console_log(vals)
    #     # self.update_warehouse_and_location()  
    #     res = super(SaleOrder, self).write(vals)

    #     return res


SaleOrder()
