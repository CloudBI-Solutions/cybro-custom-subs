# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class WebsiteConfiguration(models.Model):
    _name = "website.configuration"
    _description = "Website Configuration"

    name = fields.Char("Name")
    cart_qty_limit = fields.Integer(string='Quantity Limit')
    website_category_line = fields.One2many("website.configuration.category.line", "configuration_id",
                                            string="Website Category Line")
    home_category_ids = fields.Many2many("product.public.category", "website_configuration_product_category_ids",
                                         "configuration_id", "category_id", string="Home Category")

    website_component_line = fields.One2many("website.configuration.component.line", "configuration_comp_id",
                                             string="Website component Line")
    component_type_ids = fields.Many2many("component.type", "website_configuration_component_type_id",
                                          "configuration_id", "component_id", string="Base Component")
    accessories_type_ids = fields.Many2many("product.public.category", "product_public_category_website_rel",
                                            "category_id", "accessories_type_id", string="Accessories")

    def get_category_lower(self, line):
        categ_name = ''
        for product_id in line.products_id:
            categ_name = product_id.name
        # categ_name = line.category_id.name
        return categ_name.lower().replace(" ", "-")

    def get_product_image(self, product_id):
        return "/web/image?model=%s&id=%s&field=image_1920" % (product_id._table.replace("_", "."), product_id.id)


class WebsiteConfigurationCategoryLine(models.Model):
    _name = "website.configuration.category.line"
    _description = "Website Configuration Category Line"

    configuration_id = fields.Many2one("website.configuration", string="Configuration Id")
    category_id = fields.Many2one("product.public.category", string="Category")
    product_ids = fields.Many2many("product.product", "configuration_product_rel", "configuration_id", "product_id",
                                   string="Product(s)")


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    menu_category_ids = fields.Many2many("product.public.category", string="Menu Category")


class WebsiteConfigurationcomponentLine(models.Model):
    _name = "website.configuration.component.line"
    _description = "Website Configuration Component Line"

    configuration_comp_id = fields.Many2one("website.configuration", string="Configuration Id")
    parent_ids = fields.Many2one("component.parents.type", string="Parent component")
    sub_ids = fields.Many2many("component.type", string="Components")
