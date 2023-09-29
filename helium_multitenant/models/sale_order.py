from odoo import models, fields, api, _
from .utils import console_log
from odoo.exceptions import UserError
import datetime


class SaleOrder(models.Model):

    _name = 'sale.order'
    _inherit = 'sale.order'

    @api.multi
    def update_warehouse_and_location(self):
        # if SaleOrder is not paid
        if self.status == "draft":
            data = {}
            for attribute in self.partner_id.attribute_ids:
                data[attribute.name] = attribute.value
            # console_log(("insurance patient attributes: ", data))
            insurance_total = 0.0
            cash_total = 0.0
            if not 'location' in data or 'warehouse' in data:
                UserError("Location and Warehouse information not found")
                return

            warehouse = self.env['stock.warehouse'].search(
                [("name", "=", data['warehouse'])], limit=1)
            if not warehouse:
                return
            self.warehouse_id = warehouse[0]
            self.location_id = self.env['stock.location'].search(
                [("name", "=", data['warehouse'])])[0]
            self.pricelist_id = self.warehouse_id.pricelist


            # with the new vals, amend the sale order 
            order_line = self.order_line

            for item in order_line:
                price = self.pricelist.get_product_price(
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

            return

    # amend_sale_order

        return

    # delete from model

    # add to invoice.


SaleOrder()
