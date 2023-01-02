from odoo import fields, models


class HomeImage(models.Model):
    _name = 'home.image'
    _description = "Home Image"

    name = fields.Char(string="Name")
    image = fields.Binary(string="Image")
    description = fields.Text("Image Description")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)

    organisation_ids = fields.Many2many('organisation.organisation',
                                        string="Organisations")


class HomeGallery(models.Model):
    _name = 'home.gallery'
    _description = "Home Gallery"

    name = fields.Char(string="Name")
    image = fields.Binary(string="Image")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    organisation_ids = fields.Many2many('organisation.organisation',
                                        string="Organisations")
