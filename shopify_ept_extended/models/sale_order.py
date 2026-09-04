from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def prepare_vals_for_sale_order_line(self, product, product_name, price, quantity):
        line_vals = super().prepare_vals_for_sale_order_line(product, product_name, price, quantity)
        line_vals['price_unit'] = price/1.19
        return line_vals
