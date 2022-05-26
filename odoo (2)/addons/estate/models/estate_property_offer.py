from odoo import models, fields, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float('Price')
    state = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False, default='accepted')
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity= fields.Integer("Validity", default = "7")
    date_deadline = fields.Date("Date Deadline", inverse="_inverse_date_deadline")


    @api.depends('create_date', 'validity')
    def _inverse_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + record.validity

    _sql_constraints = [
        ('price', 'CHECK(price > 0)',
         'Price should be positive')
    ]

    def action_confirm(self):
        for record in self:
            record.state = record.state('accepted')
            record.property_id.selling_price = record.price
        return True
    
    def action_refuse(self):
        for record in self:
            record.state = record.state('refused')
            record.property_id.selling_price = 0.00
        return True
   