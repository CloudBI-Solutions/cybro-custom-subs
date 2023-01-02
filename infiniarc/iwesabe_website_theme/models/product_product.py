# -*- coding: utf-8 -*-
import string

from openpyxl.worksheet import related

from odoo import api, models, fields, _
import json
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def default_get(self, fields):
        res = super(ProductTemplate, self).default_get(fields)
        component_lines = []
        if res.get('type_of_pc', False) == 'customize':
            for line in self.env['component.type'].search([('is_default', '=', True)]):
                product_id = False
                if line.product_line.sorted(key=lambda r: r.list_price):
                    product_id = line.product_line.sorted(key=lambda r: r.list_price)[0].id
                component_lines.append((0, 0, {'component_id': line.id,
                                               'parent_category_id': line.parent_category_id.id,
                                               'product_ids': [(6, 0, line.product_line.ids)],
                                               'product_id': product_id,
                                               }))
        res['component_lines'] = component_lines
        return res
    is_default_cust = fields.Boolean()
    type_products = fields.Selection([('normal', 'Normal'), ('customized', 'Customized')], string='Type of Products',
                                     default='normal')

    type_of_pc = fields.Selection([('normal', 'Not Customizable'), ('customize', 'Customizable')],
                                  string='Type of Product PC', default='normal')
    component_lines = fields.One2many('component.line', 'product_tmp_id', 'Components Line')
    accessories_lines = fields.One2many('component.line', 'accessories_product_tmpl_id', 'Accessories Line')
    specification_line = fields.One2many('specification.item.line', 'product_id', 'Specification Line')

    component_id = fields.Many2one('component.type', 'Component', tracking=True)
    parents_type = fields.Many2one("component.parents.type", string='parents component', related='component_id.parents_type')
    brand_id = fields.Many2one('brand.brand', string="Brand", tracking=True)
    micro_store_id = fields.Many2one('dynamic.micro.store', string="Dynamic Micro Store")
    sales_price = fields.Float(string="Sales Price")
    gaming_pc = fields.Boolean(string='PC')

    # New form fields
    arabic_name = fields.Char("Arabic Name", tracking=True)
    quantity = fields.Float("Quantity", tracking=True)
    min_delivery_days = fields.Integer("Min Delivery Days", tracking=True)
    max_delivery_days = fields.Integer("Max Delivery Days", tracking=True)
    is_free_shipping_pc_builder = fields.Selection([('yes', 'Yes'), ('no', 'No')], "Is it Free shipping PC Builder?")
    is_ready_to_ship = fields.Selection([('yes', 'Yes'), ('no', 'No')], "Is Ready to Ship?")
    is_nvidia_micro_store = fields.Boolean("Is this an NVIDIA product for the micro store?")
    is_featured_pc_builder = fields.Boolean("Is it Featured PC Builder?")
    terms_of_use_arabic = fields.Text("Terms of Use in Arabic")
    is_gear_store = fields.Boolean("Is Gear Store Product")
    unfit_product_msg = fields.Text("Message of the unfit product")
    relative_product_ids = fields.Many2many('product.product', string="Products")

    # PC Built Components Restrictions
    power_watt = fields.Integer("Power Watts", tracking=True)
    type_of_restrictions = fields.Selection([('is_cpu', 'CPU'),
                                             ('is_motherboard', 'Motherboard'),
                                             ('is_cooler', 'Cooler'),
                                             ('is_case', 'Case'),
                                             ('is_memory', 'Memory'),
                                             ('is_fans', 'Fans'),
                                             ('is_power_suplly', 'Power Supply'),
                                             ('m_2', 'M.2')], string='Type Restrictions')
    is_cpu = fields.Boolean("CPU")
    is_motherboard = fields.Boolean("Motherboard")
    is_cooler = fields.Boolean("Cooler")
    is_case = fields.Boolean("CASE")
    is_memory = fields.Boolean("MEMORY")
    is_fans = fields.Boolean("FANS")
    is_power_suplly = fields.Boolean("POWER SUPLLY")

    cpu_type_id = fields.Many2one("cpu.type", string="CPU Type")
    support_oc = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Support OC', default='no')
    water_cooling_ids = fields.Many2many('radiator.size.values', 'radiator_size_values_water_rel', 'product_id',
                                         'water_id', string='Water-cooling')
    is_k_type = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Is K Type', default='no')
    memories_type_support_id = fields.Many2one("memories.type", string="Memories Type Support")
    cpu_support_id = fields.Many2one("cpu.type", string="CPU Support")
    no_of_support = fields.Integer('Number of m.2 Support')
    serics_motherboard = fields.Selection([('h', 'H'), ('b', 'B'), ('z', 'Z')], string='Series Mother-Board',
                                          default='h')
    motherboard_ids = fields.Many2many('product.product', 'product_product_motherboard_rel', 'product_id',
                                       'motherboard_id', string='Motherboard')
    # memory_type = fields.Many2one('memories.type', string='Memory Type')

    type_cooler = fields.Selection([('air_cooler', 'Air Cooler'), ('water_cooler', 'Water Cooler')],
                                   string='Cooler Type', default='air_cooler')
    air_height = fields.Integer('Height')
    radiator_size_id = fields.Many2one("radiator.size.values", string="Radiator Size")

    type_cooler_support = fields.Selection(
        [('both', 'Both Cooler'), ('air_cooler', 'Air Cooler'), ('water_cooler', 'Water Cooler')],
        string='Cooler Type Support', default='air_cooler')
    water_cooler_ids = fields.Many2many('product.product', 'product_product_water_cooler_rel', 'product_id',
                                        'water_cooler_id', string='Water Cooler')
    air_cooler_height = fields.Integer('Air cooler Height support')
    radiator_size_ids = fields.Many2many("radiator.size.values", string="Radiator Size Values")
    fans_no_support = fields.Integer('Fans Number Support')
    built_fans_no = fields.Integer('Built in fans No.')

    memories_type_id = fields.Many2one("memories.type", string="Memories Type")

    pak_fans_no = fields.Integer('Package Fans No.')
    power_value_support = fields.Integer('Power Value Support')

    no_of_fans = fields.Integer('Number of Fans')

    best_seller = fields.Boolean(help="Enable the field to display as best sellers")

    def action_product_public(self):
        if self.is_published:
            self.is_published = False
        else:
            self.is_published = True

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        default['component_lines'] = self.component_lines.ids
        default['standard_price'] = self.standard_price
        default['standard_price'] = self.standard_price
        return super(ProductTemplate, self).copy(default=default)

    @api.model
    def create(self, vals):
        print('self.gaming_pc', self.gaming_pc)
        res = super(ProductTemplate, self).create(vals)
        component_id = vals.get('component_id', False)
        if component_id:
            component_id = self.env['component.type'].browse(component_id)
            component_id.message_post(body='New ADD Product  :- ' + str(res.name),
                                      author_id=self.env.user.partner_id.id)
        if self.gaming_pc ==True:
            self.filter_type = 'Gaming PC'

        return res

    def write(self, vals):
        component_id = vals.get('component_id', False)
        if component_id:
            component_id = self.env['component.type'].browse(component_id)
            component_id.message_post(body='New ADD Product  :- ' + str(self.name),
                                      author_id=self.env.user.partner_id.id)
        return super(ProductTemplate, self).write(vals)

    @api.onchange('component_lines')
    def _check_component(self):
        for rec in self:
            for line in rec.component_lines:
                order_line_ids = rec.component_lines.filtered(lambda pr: pr.component_id.id == line.component_id.id)
                if len(order_line_ids) > 1:
                    raise UserError("'Exists!!', This Component is already added")


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_allowed_components = fields.Boolean("Allowed Components")

    def get_json_data(self):
        data = {
            "product_name": self.name,
            "price": '{0:.2f}'.format(self.list_price)
        }
        return json.dumps(data)

    def name_get(self):
        if self._context.get("show_price"):
            result = []
            for rec in self:
                name = "%s [ %s ] [ %s ]" % (rec.name, rec.list_price, rec.qty_available)
                result.append((rec.id, name))
            return result
        else:
            return super(ProductProduct, self).name_get()


class DynamicMicroStore(models.Model):
    _name = "dynamic.micro.store"
    _description = "Dynamic Micro Store"

    name = fields.Char('Name')


class ComponentType(models.Model):
    _name = "component.type"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Product Components Type"

    image = fields.Binary('Image', help="Image")
    name = fields.Char('Name', tracking=True)
    code = fields.Char('Code', tracking=True)
    sequence = fields.Integer('Sequence', default=1, tracking=True)
    is_default = fields.Boolean('is Default', tracking=True)
    allowed_to_multiple = fields.Boolean('Allowed to Multiple', tracking=True)
    category_ids = fields.Many2many('component.category', 'component_category_rel', 'component_id', 'category_id',
                                    string="Category")
    product_line = fields.One2many('product.product', 'component_id', string="Products")
    web_view_type = fields.Selection([('grid', 'Grid'), ('list', 'List')], string='Web View Type', default='grid',
                                     tracking=True)
    type = fields.Selection([('components', 'Components'), ('accessories', 'Accessories')], string="Type")
    parent_category_id = fields.Many2one('product.public.category', string="Section / Parent Category", tracking=True)
    parents_type = fields.Many2one("component.parents.type", string='parent component', tracking=True)


    # value_id = fields.Many2one('component.filter')
    # values = fields.Char(string='Values')
    # product_id = fields.Many2many('product.template', 'name')


class ComponentParentsType(models.Model):
    _name = 'component.parents.type'
    _rec_name = 'name'
    _description = 'Component Parent Type'

    name = fields.Char(string='Name')


class ComponentCategory(models.Model):
    _name = "component.category"
    _description = "Product Components Category"

    name = fields.Char('Name')


#

class ComponentLine(models.Model):
    _name = "component.line"
    _description = "Components Line"

    sequence = fields.Integer(index=True,
                              help="Gives the sequence order when displaying a list of bank statement lines.",
                              default=1)
    product_ids = fields.Many2many('product.product', 'product_component_line_rel', 'component_id', 'product_id',
                                   string="Products")
    component_id = fields.Many2one('component.type', 'Category')
    product_tmp_id = fields.Many2one('product.template', 'Product Component')
    product_id = fields.Many2one("product.product", string="Default One")
    accessories_product_tmpl_id = fields.Many2one('product.template', 'Accessories Product')
    parent_category_id = fields.Many2one('product.public.category', string="Section / Parent Category")

    allowed_number = fields.Integer('No. of selections', default=1)
    allowed_number_qty = fields.Integer('No. of Quantities', default=1)
    allowed_multi_sel = fields.Boolean('Allowed Number of Quantities')
    mandatory_category = fields.Boolean('Mandatory Category', default=True)
    mandatory_all = fields.Boolean('Mandatory All')

    @api.onchange('product_ids')
    def get_default_product(self):
        for rec in self:
            if rec.product_ids:
                rec.product_id = rec.product_ids.sorted(key=lambda r: r.list_price).ids[0]

    def get_products(self):
        for rec in self:
            rec.product_ids = rec.component_id.product_line.ids

    def del_products(self):
        for rec in self:
            rec.product_ids = [(5,)]

    def get_barnd_name(self):
        brands = []
        # for c in self.component_lines:
        for p in self.product_ids:
            if p.brand_id:
                brands.append(p.brand_id)
        return list(set(brands))
