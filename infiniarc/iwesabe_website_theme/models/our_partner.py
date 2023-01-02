# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class OurPartner(models.Model):
    _name = "our.partner"
    _description = "Our Partner"

    sequence = fields.Integer("Sequence", required=True, default=1)
    name = fields.Char('Name', required=True, translate=True)
    image = fields.Binary('Image')
    website_published = fields.Boolean('Visible in Portal / Website', copy=False, default=True)

    def toggle_website_published(self):
        self.website_published = False if self.website_published else True
