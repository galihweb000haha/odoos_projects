import string
import random
from odoo import models, fields, _

class CouponPos(models.Model):
    _name = 'coupon.pos'
    def generate_code(self):
        size = 8
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    _sql_constraints = [
        ('name_uniq', 'unique (code)', "Code already exists !"),
    ]

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", default=generate_code)
    expiry_date = fields.Date(string="Expiry Date", required=True, help='The expiry date of Coupon.')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    disc_amount = fields.Monetary(string="Discount Amount")
    



