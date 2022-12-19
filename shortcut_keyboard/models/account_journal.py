from odoo import fields, models

class AccountJournal(models.Model):
    _inherit = 'account.journal'
    _description = 'Adding M2O field for shortcut'

    shortcut_payment_id = fields.Many2one('pos.shortcut.config')

    def get_shortcut_code(self, ids):
        pos_shortcut_config_code = []
        for id in ids:
            pos_payment_method_ids = self.env['account.journal'].search([('pos_payment_method_ids', '=', id)])
            pos_shortcut_config_code.append(pos_payment_method_ids.shortcut_payment_id.code)

        return {'code':pos_shortcut_config_code, 'ids':ids}
