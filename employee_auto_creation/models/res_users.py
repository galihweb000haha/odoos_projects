from odoo import models, fields
from ast import literal_eval

class Users(models.Model):
    _inherit = 'res.users'

    birthday = fields.Date('Date of Birth', groups="hr.group_hr_user", tracking=True, store=True)
    identification_id = fields.Char(string='Identification No', groups="hr.group_hr_user", tracking=True, store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups="hr.group_hr_user", default="male", tracking=True, store=True)
    place_of_birth = fields.Char('Place of Birth', groups="hr.group_hr_user", tracking=True, store=True)
    country_of_birth_id = fields.Many2one('res.country', string="Country of Birth", groups="hr.group_hr_user", tracking=True, store=True)
    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', groups="hr.group_hr_user", tracking=True, store=True)

    def write(self, vals):
        """
            Employee will be created automatically if conditions is fullfiled
        """
        create_employee = self.env['ir.config_parameter'].sudo().get_param('employee_auto_creation.create_employee', default=False)
        if create_employee:
            # get field from config parameter
            field_ids = literal_eval(self.env['ir.config_parameter'].sudo().get_param('employee_auto_creation.field_ids', default=False))
            # check whether employee is already created
            is_employee = self.env['hr.employee'].search([('user_id', '=', self.id)])
            if not is_employee:
                # set mandatory field
                mandatory_field_dict = {
                    'name': self.name,
                    'user_id': self.id,
                }

                if field_ids:
                    # get field id from database
                    field_obj = self.env['ir.model.fields'].browse(field_ids)

                    comp_field_resusers_hremployee = {
                        'login': 'work_email',
                        'many2one.company_id': 'company_id',
                        'birthday': 'birthday',
                        'identification_id': 'identification_id',
                        'gender': 'gender',
                        'place_of_birth': 'place_of_birth',
                        'many2one.country_of_birth_id': 'country_of_birth',
                        'many2one.country_id': 'country_id'
                    }

                    temp_dict = {}
                    for val in field_obj:    
                        for key, value in comp_field_resusers_hremployee.items():
                            if value == val.name:
                                temp_dict[key] = val.name

                    temp_dict2 = {}
                    for key, value in temp_dict.items():
                        split_key = key.split(".")
                        if len(split_key) > 1:
                            if split_key[0] == 'many2one':
                                val = getattr(self, split_key[1]).id
                        else:
                            val = getattr(self, key)
                            
                        temp_dict2[value] = val

                    # merge dictionary
                    mandatory_field_dict.update(temp_dict2)
                
                # create hr employee
                self.env['hr.employee'].create(mandatory_field_dict)

        return super(Users, self).write(vals) 