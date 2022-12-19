from odoo import fields, models, api
import midtransclient, random, string
from odoo.http import request


def _partner_split_name(partner_name):
    return [' '.join(partner_name.split()[:-1]), ' '.join(partner_name.split()[-1:])]

class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('midtrans', 'Midtrans')])
    merchant_code = fields.Char(string="Merchant Code")
    
    server_key = fields.Char(string="Server Key", required=True)
    client_key = fields.Char(string="Client Key", required=True)

    def get_payment_acquirer_state(self):
        return self.state
    
    @api.onchange('state')
    def on_change_state(self):
        self.server_key = ''
        self.client_key = ''


class TxMidtrans(models.Model):
    _inherit = 'payment.transaction'

    token_transaction = fields.Char()
    redirect_url = fields.Char()

    def payment_midtrans_transaction(self):
        """
            create detail transaction
        """
        
        last_tx_id = request.session.get('__website_sale_last_tx_id')
        midtrans = self.env['payment.acquirer'].search([('provider', '=', 'midtrans')])
    
        snap = midtransclient.Snap(
            is_production = False if midtrans.state == 'test' else True,
            server_key = midtrans.server_key,
            client_key = midtrans.client_key,
        )

        payment_transaction = self.env['payment.transaction'].browse(last_tx_id)

        letters = string.ascii_letters
        order_id = ''.join(random.choice(letters) for i in range(10))+':'+payment_transaction.reference
        
        param = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": int(payment_transaction.amount),
                "currency": "IDR",
            }, "credit_card":{
                "secure" : True
            },
            "customer_details": {
                "first_name": _partner_split_name(payment_transaction.partner_name)[0],
                "last_name": _partner_split_name(payment_transaction.partner_name)[1],
                "email": payment_transaction.partner_email,
                "phone": payment_transaction.partner_phone
            }
        }     
        
        transaction = snap.create_transaction(param)
        
        self.token_transaction = transaction['token']
        self.redirect_url = transaction['redirect_url']

        return transaction
  