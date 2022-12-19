# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Contacts(models.Model):
    _name = 'academy.contacts'

    name = fields.Char()
    title = fields.Char()
    age = fields.Integer()
    description = fields.Text()