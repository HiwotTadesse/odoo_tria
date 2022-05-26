from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name desc"


    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color Index', default=0)

    

    _sql_constraints = [
        ('name', 'UNIQUE(name)',
         'Name should be Unique')
    ]