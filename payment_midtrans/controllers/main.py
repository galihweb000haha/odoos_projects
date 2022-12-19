import midtransclient
import json
from odoo import http
from odoo.http import request

class PayMidtransController(http.Controller):
    @http.route('/payment/midtrans/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def midtrans_webhook(self, **data):
        """
            to catch response from midtrans notification of payment
        """
        midtrans = request.env['payment.acquirer'].search([('provider', '=', 'midtrans')])
    
        api_client = midtransclient.CoreApi(
            is_production = False if midtrans.state == 'test' else True,
            server_key = midtrans.server_key,
            client_key = midtrans.client_key,
        )
        
        data = json.loads(request.httprequest.data)

        status_response = api_client.transactions.notification(data)

        order_id = status_response['order_id']
        transaction_status = status_response['transaction_status']

        reference = order_id.split(':')[1] 
        payment_tx = http.request.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        
        if transaction_status == 'settlement':
            payment_tx.state = 'done'
        elif transaction_status == 'pending':
            payment_tx.state = 'pending'
        elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
            payment_tx.state = 'cancel'

        return http.Response(status=200)

