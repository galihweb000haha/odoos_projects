from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_customer_url(self):
        """
        this function will return certain url customer page based on partner id in argument.
        """
        return self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/web#id=' + str(self.partner_id.id) + '&action=208&model=res.partner&view_type=form&cids=1&menu_id=211' 

    def confirm_quotation(self):
        """
        change the state of sale order from sent to sale, then return route to sale order portal.
        """
        if self.state == 'sent':
            self.state = 'sale'
        return "/my/orders/" + str(self.id)