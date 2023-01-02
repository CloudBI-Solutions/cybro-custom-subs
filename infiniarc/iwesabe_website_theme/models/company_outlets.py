from odoo import api, models, fields


class CompanyOutlets(models.Model):
    _name = "company.outlets"
    _description = 'Company Outlets'

    name = fields.Char(string='Outlet', required=True)
    parent_id = fields.Many2one('res.company', string='Parent Company', default=lambda self: self.env.company)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one(
        'res.country.state',
        string="Fed. State", domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country',
                                 string="Country")
    email = fields.Char(related='parent_id.email', store=True, readonly=False)
    phone = fields.Char('Outlet Phone no:', store=True, readonly=False)
    mobile = fields.Char('Outlet Mobile no:', store=True, readonly=False)
    website = fields.Char(related='parent_id.website', readonly=False)
    # store_latitude = fields.Float(string="Outlet Latitude", digits=(10, 7))
    # store_longitude = fields.Float(string="Outlet Longitude", digits=(10, 7))
    text = fields.Html(string='Description', readonly=True)

