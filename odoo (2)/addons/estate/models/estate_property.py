from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Date Availablity', default=lambda self: fields.Datetime.now()+ relativedelta(months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly= True,copy=False)
    bedrooms = fields.Integer('Bed Rooms', default = 2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([('n','North'), ('s','South'), ('e','East'),('w','West')], 'Garden Orientation')
    active = fields.Boolean('Active', default = False)
    state = fields.Selection([('new', 'New'), ('offer_r', 'Offer Received'), ('offer_a', 'Offer Accepted'), ('sold', 'Sold '), ('canceled', 'Canceled')], required=True, copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type', string= 'Property Type')
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Partner")
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer("Total Area", compute="_compute_total")
    best_price = fields.Float('Best Price', compute="_compute_bestPrice")
    status = fields.Char('Status', default='New')
    

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)',
         'Expected price should be positive'),
        ('selling_price', 'CHECK(selling_price > 0)', 
         'Selling price should be positive')
    ]


    @api.depends("living_area", "garden_area", "offer_ids.price")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area * record.garden_area

    def getMax(array):
        return max(array)

    @api.depends("offer_ids")
    def _compute_bestPrice(self):
        best_price = 0  
        for record in self.offer_ids:  
            if(best_price < record.price):
                best_price = record.price
        self.best_price = best_price
            #record.best_price = max(record.offer_ids,  lambda k: record.offer_ids[k].price)

    @api.onchange("garden")
    def __onchange_garden(self):
            self.garden_area = 10

    def action_cancel(self):
        for record in self:
            record.status = "New"
        return True
    
    def action_sold(self):
        for record in self:
            record.status = "Sold"
        return True

    @api.constrains('selling_price')
    def _check_offer_percentage(self):
        for record in self:
            if record.selling_price <= (record.expected_price/90):
                raise ValidationError("The selling price cannot be lower than 90 expected price")

    