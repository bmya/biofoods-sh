from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    commercial_agreements = fields.Float(string='Commercial Agreements %', tracking=True)
