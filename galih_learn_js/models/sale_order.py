from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"
    def get_last_order_amount(self):
        value = 0
        for order in self:
            value += order.amount_total
        return value