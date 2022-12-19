from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_promo = fields.Boolean(string='Is Promotion Product', default=False, required=True)
