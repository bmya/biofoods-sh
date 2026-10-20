from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    margin_taxed = fields.Float('Net Margin')
    commercial_agreements = fields.Float(string='Commercial Agreements %', group_operator='max')
    price_unit = fields.Float('Unit Price')
    purchase_price = fields.Float(string='Unit Cost', groups="account.group_account_manager")

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['margin_taxed'] = (
            "SUM((l.margin + l.price_tax * l.margin_percent) / CASE "
            "COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)"
        )
        res['commercial_agreements'] = "s.commercial_agreements"
        res['price_unit'] = (
            "CASE WHEN l.product_id IS NOT NULL THEN sum(l.price_unit / CASE "
            "COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) ELSE 0 END"
        )
        res['purchase_price'] = (
            "CASE WHEN l.product_id IS NOT NULL THEN sum(l.purchase_price / CASE "
            "COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) ELSE 0 END"
        )
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            partner.commercial_agreements,
            l.price_unit,
            l.purchase_price
            """
        return res
