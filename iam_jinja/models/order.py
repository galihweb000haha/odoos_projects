from odoo import models, fields
from jinja2 import Environment

class Order(models.Model):
    _inherit = "sale.order"

    def fields_view_get(self, *args, **kwargs):
        res = super().fields_view_get(*args, **kwargs)

        templater = Environment(
            variable_start_string="{{{",
            variable_end_string="}}}"
        )

        template = templater.from_string(res["arch"])

        res["arch"] = template.render(
            message="Hello Galih"
        )

        return res