from odoo import models, fields

class PosOrderReport(models.Model):
    _inherit ='report.pos.order'

    salesperson_id = fields.Many2one('hr.employee')

    def _select(self):
        select = super(PosOrderReport, self)._select() 
        return select + ',s.salesperson_id AS salesperson_id'

    def _group_by(self):
        group_by = super(PosOrderReport, self)._group_by() 
        return group_by + ',s.salesperson_id'