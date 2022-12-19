from odoo import api, fields, models, _

class PosOrder(models.Model):
    _inherit = 'pos.order'

    salesperson_id = fields.Many2one("hr.employee", string="Salesperson")

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['salesperson_id'] = ui_order['pos_session_id']
        return order_fields
