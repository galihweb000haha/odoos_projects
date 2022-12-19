from dbm.ndbm import library
from odoo import models, fields

class GuestBook(models.Model):
    _name = "guest.book"
    
    complete_name = fields.Char(string='Complete Name')
    phone_number = fields.Char(string='Phone')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male')
    library_id = fields.Many2one('library.book', string="Library", required=True)
    email = fields.Char(string='Email')
    necessity = fields.Text(string='Necessity')