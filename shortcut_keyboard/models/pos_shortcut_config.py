from odoo import models, fields

class PosShortcutConfig(models.Model):
    _name = 'pos.shortcut.config'
    _description = 'model to save these shortcut configuration'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")

    