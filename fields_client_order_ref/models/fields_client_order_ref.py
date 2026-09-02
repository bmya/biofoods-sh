from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        res = super().write(vals)
        if 'client_order_ref' in vals:
            for picking in self.picking_ids.filtered(lambda p: p.state != 'cancel' and self.client_order_ref != p.client_order_ref):
                picking.write({'client_order_ref': self.client_order_ref})
            for move in self.invoice_ids.filtered(lambda i: i.state != 'cancel' and self.client_order_ref != i.ref):
                move.write({'ref': self.client_order_ref})
        return res


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    client_order_ref = fields.Char('Referencia cliente')


class AccountMove(models.Model):
    _inherit = 'account.move'

    def write(self, vals):
        res = super().write(vals)
        if 'ref' in vals:
            sales_ids = self.invoice_line_ids.mapped('sale_line_ids').mapped('order_id')
            for sale in sales_ids:
                if self.ref != sale.client_order_ref:
                    sale.write({'client_order_ref': self.ref})
            for picking in sales_ids.mapped('picking_ids'):
                if self.ref != picking.client_order_ref:
                    picking.write({'client_order_ref': self.ref})
        return res


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        res = super(StockMove, self)._get_new_picking_values()
        client_order_ref = self.env['sale.order'].search_read([('name', '=', res.get('origin', None))], ['client_order_ref'])
        if client_order_ref:
            res['client_order_ref'] = client_order_ref[0]['client_order_ref']
        return res
