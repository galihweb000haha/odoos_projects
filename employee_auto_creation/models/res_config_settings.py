from odoo import  models, fields, api, _
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    create_employee = fields.Boolean(string="Create Employee", default=False, config_parameter='employee_auto_creation.create_employee')
    
    # def field_user_domain(self):
    #     """
    #         make a domain to filter model_id and some allowed fields
    #     """
    #     res_users_id = self.env.ref('hr.model_hr_employee').id
    #     return [('model_id', '=', res_users_id), ('name', 'in', (
    #         'work_email', 
    #         'company_id', 
    #         'birthday',
    #         'identification_id',
    #         'gender',
    #         'place_of_birth',
    #         'country_of_birth_id',
    #         'country_id'
    #     ))]
        
    field_ids = fields.Many2many('ir.model.fields',
    domain=lambda self: [('model_id', '=', self.env.ref('hr.model_hr_employee').id), ('name', 'in', (
            'work_email', 
            'company_id', 
            'birthday',
            'identification_id',
            'gender',
            'place_of_birth',
            'country_of_birth_id',
            'country_id'
        ))], string='Users', store=True, 
    help="Optional tags you may want to assign for custom field")
  
    @api.model
    def set_values(self):
        """
            set param auto_create_employee and field_ids 
        """
        field_ids = self.field_ids.ids

        self.env['ir.config_parameter'].sudo().set_param('employee_auto_creation.field_ids', field_ids)
        
        self.env['ir.config_parameter'].sudo().set_param('employee_auto_creation.create_employee', self.create_employee)
        
        super(ResConfigSettings, self).set_values()

    @api.model
    def get_values(self):
        """
            get param fields id then update filed_ids value with selected fields
        """
        res = super(ResConfigSettings, self).get_values()

        selected_fields = self.env['ir.config_parameter'].sudo().\
            get_param('employee_auto_creation.field_ids', default=False)
        
        res.update(
            field_ids = [(6, _, literal_eval(selected_fields))]
        )

        return res
  	

         