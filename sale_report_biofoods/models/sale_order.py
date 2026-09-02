from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    commercial_agreements = fields.Float(string='Commercial Agreements %', tracking=True, readonly=True)

    def action_confirm(self):
        for so in self:
            so.commercial_agreements = so.partner_id.commercial_partner_id.commercial_agreements
        return super().action_confirm()
