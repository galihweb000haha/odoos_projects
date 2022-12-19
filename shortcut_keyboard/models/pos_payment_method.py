from odoo import fields, models

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'
    _description = 'inherit pos payment method, addding field shortcut'

    shortcut = fields.Char(related='cash_journal_id.shortcut_payment_id.name')


