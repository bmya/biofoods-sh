from . import models


def _update_client_order_ref(env):
    sales = env['sale.order'].search([('client_order_ref', '!=', '')])
    for sale in sales:
        pickings = sale.picking_ids
        pickings.write({'client_order_ref': sale.client_order_ref})
