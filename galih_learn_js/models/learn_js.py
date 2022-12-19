from odoo import models, fields

class LearnJs(models.Model):
    _name = 'learn.js'
    _description = 'Galih Learn Javascript'

    field_one = fields.Integer('Field One', default=1)
    field_two = fields.Integer('Field Two', default=1)
    field_three = fields.Integer('Field Three', default=1)