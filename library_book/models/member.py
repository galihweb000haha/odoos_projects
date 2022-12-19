from odoo import models, fields


class Member(models.Model):
    _name = 'member'

    name = fields.Char(string='Complete Name')
    email = fields.Char(string='Email', placeholder='youremail@mail.com')
    birthday = fields.Date(string='Birthday')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male')
    address = fields.Text(string='Address')