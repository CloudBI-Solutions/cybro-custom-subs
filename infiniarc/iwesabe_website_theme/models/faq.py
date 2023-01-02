from odoo import fields, models, api, _


# class UserCreation(models.Model):
#     _inherit = 'res.users'
#
#     otp = fields.Char(string='OTP')
#     otp_time = fields.Datetime(string='OTP Time')


class SpecialOffer(models.Model):
    _name = 'special.offer'
    _description = 'Special Offer'

    name = fields.Char(string='Name')


class WebsiteConfigurationModels(models.Model):
    _inherit = "website.configuration"
    _description = "Website Configuration"

    website_model_line = fields.One2many("product.model", "web_id",
                                         string="Website Models")


class WebsiteProductModel(models.Model):
    _name = 'product.model'
    _description = 'Website Product Model'

    web_id = fields.Many2one('website.configuration')
    filter_id = fields.Many2one('product.filter')
    products_id = fields.Many2many('product.template')

    def get_categorys_lower(self, line):
        categ_name = line.products_id.filter_type
        return categ_name.lower().replace(" ", "-")


class ProductDescription(models.Model):
    _inherit = 'product.template'

    product_description = fields.Char(string='Product Description')
    extra_info = fields.Char(string='Extra Info')
    terms = fields.Char(string='Terms And Conditions')
    best = fields.Boolean(string='Best Seller')
    value_id = fields.Many2many('desktop.filter.line', string='Desktop Filter')

    stock_clearance = fields.Boolean(string='Stock Clearance')
    arrival = fields.Boolean(string='New Arrival')
    special_offer = fields.Boolean(string='Special offer')
    special_offer_filter = fields.Many2one('special.filter')
    offer_percent = fields.Float(string='Offer Percentage', compute='_compute_offer_percent')
    document_ids = fields.Many2many('ir.attachment', string="Documents",
                                    domain="[('mimetype', 'not in', ('application/javascript','text/css'))]")

    def _compute_offer_percent(self):
        for rec in self:
            rec.offer_percent = rec.sales_price - ((rec.sales_price * rec.list_price)/100)


class InfiniarcFaq(models.Model):
    _name = 'faq.faq'
    _rec_name = 'question'
    _description = 'Infiniarc Faq'

    question = fields.Char(string='Question')
    answer = fields.Char(string='Answer')
    type = fields.Selection([('faq', 'FAQs'), ('knowledge', 'Knowledge Base')],
                            string='Type', default='faq')


class InfiniarcCompanyPolicy(models.Model):
    _name = 'terms.and.conditions'
    _rec_name = 'types'
    _description = 'Terms And Condition'

    terms = fields.Char(string='Description')
    policy = fields.Char(string='Privacy Policy')
    shipping = fields.Char(string='Shipping Policy')
    types = fields.Char(string="Policy")
    type = fields.Selection(
        [('terms', 'Terms And Conditions'), ('privacy', 'Privacy Policy'), ('shipping', 'Shipping Policy')])


class InfiniarcPolicy(models.Model):
    _name = 'infiniarc.policy'
    _description = 'Infiniarc Company Policy'
    _rec_name = 'policy'

    policy = fields.Char(string='Name', required=True)
    description = fields.Html(string='Policy')
    type = fields.Many2one('terms.and.conditions', string='Type')


class InfiniarcWarranty(models.Model):
    _name = 'warranty.warranty'
    _rec_name = 'type'
    _description = 'Infiniarc Warranty'

    type = fields.Char(string='Type')
    description = fields.Html(string='Description')


class DriverDownload(models.Model):
    _name = 'driver.download'
    _rec_name = 'driver'
    _description = 'Driver Download'

    driver = fields.Char('Driver')
    description = fields.Char('Description')


class InfiniarcAnnouncement(models.Model):
    _name = 'infiniarc.announcement'
    _description = 'Infiniarc Announcement'
    _rec_name = 'announcement'

    announcement = fields.Text(string='Announcement')
