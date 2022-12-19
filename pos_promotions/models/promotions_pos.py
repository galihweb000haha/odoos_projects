from odoo import models, fields, api

class promotionsPoS(models.Model):
    _name = 'promotions.pos'
    _description = """
        manage promotional offers
    """
    _sql_constraints = [
        (
            'condition_unique',
            'unique (condition)',
            "Condition already exists !",
        ),
    ]
    condition =  fields.Selection(
        [
            ('new_customer', 'New Customer'),
            ('specific_date', 'Specific Date'),
            ('minimum_amount', 'Minimum Amount'),

        ], string='Condition', required=True, default='new_customer')
    gift_type = fields.Selection(
        [
            ('specific_product', 'get specific product'),
            ('discount', 'get discount'),

        ], string='Gift Type', required=True, default='discount')
    amount = fields.Integer(name='Amount', required=True)
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    product_id = fields.Many2one('product.product', string='Product', 
                                domain=[("is_promo", "=", True)])
    currency_id = fields.Many2one('res.currency', string="Currency",
                                related='company_id.currency_id',
                                default=lambda
                                self: self.env.user.company_id.currency_id.id)
    disc_amount = fields.Monetary(name='Discount Amount', required=True)
    spec_date = fields.Date(name='Special Date')
    min_amount = fields.Monetary(name='Minimum Amount')

   




