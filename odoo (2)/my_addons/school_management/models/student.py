from odoo import models, fields
class StudentStudent(models.Model):
   _name = 'student.student'
   name = fields.Char(string='Name', required=True)
   age = fields.Integer(string='Age')
   photo = fields.Binary(string='Image')
   gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], string='Gender')
   student_dob = fields.Date(string="Date of Birth")