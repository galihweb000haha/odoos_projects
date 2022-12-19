from odoo import http, fields
from odoo.http import request
import json

class PurchaseOrderApi(http.Controller):
    @http.route('/purchase/search', auth='none', methods=['GET'], type='json', csrf=False)
    def search(self, **kwargs):
        purchase_obj = request.env['purchase.order']
        purchase_id = purchase_obj.sudo().search([('name', '=', kwargs.get('po_number'))])
        
        line_data = []
        for line in purchase_id.order_line:
            line_data.append({
                'product_code': line.product_id.default_code,
                'price': line.price_unit,
                'qty': line.product_qty
            })

        data = {
            'po_number': purchase_id.name,
            'vendor': purchase_id.partner_id.name,
            'order_line': line_data
        }

        return {
            'code': '200',
            'status': 'success',
            'data': data
        }

    @http.route('/purchase/create', auth='api_key', methods=['POST'], type='json', csrf=False)
    def create(self, **kwargs):
        partner_obj = request.env['res.partner']
        partner_name = kwargs.get('vendor')
        partner_id = partner_obj.search([('name', '=', partner_name)]).id
        if not partner_id:
            return {
                'code': '404',
                'status': 'failed',
                'message': "Vendor '%s' not found " % (partner_name)
            }
        po_line_vals = []
        product_obj = request.env['product.product']
        for line in kwargs.get('order_line'):
            product_code = line.get('order_code')
            product_id = product_obj.search(['deafult_code', '=', product_code]).id
            if not product_id:
                return {
                    'code': '404',
                    'status': 'failed',
                    'message': "Product '%s' not found " % (product_code)
                }
                po_line_vals.append((0, 0, {
                    'product_id': product_id,
                    'product_qty': line.get('quantity'),
                    'price_unit': line.get('price')
                }))
        po_vals = {
            'partner_id': partner_id,
            'date_order': fields.datetime.now(),
            'order_line': po_line_vals
        }
        return {
            'code': '200',
            'status': 'success',
            'message': "Purchase orde '%s' success to created " % (purchase_id.name)
        }
