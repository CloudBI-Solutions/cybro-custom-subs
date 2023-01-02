from odoo import fields, models, api, _


class HomePageBanner(models.Model):
    _name = 'home.banner'
    _description = 'Home page Banner'
    _rec_name = 'name'

    banner = fields.Binary(string='Banner')
    name = fields.Char(string='Name')
    show = fields.Boolean(string='Show on Website')


class HomePageSmallBanner(models.Model):
    _name = 'home.small.banner'
    _description = 'Home page Small Banner'
    _rec_name = 'name'

    small_banner = fields.Binary(string='Small Banner')
    name = fields.Char(string='Name')
    show = fields.Boolean(string='Show on Website')


class BannerSlider(models.Model):
    _name = 'home.banner.slider'
    _description = 'Home page Banner Slider'
    _rec_name = 'name'

    banner_slider = fields.Binary(string='Small Banner')
    name = fields.Char(string='Name')
    show = fields.Boolean(string='Show on Website')


class MicroDynamicDealsBanner(models.Model):
    _name = 'micro.dynamic.deals.banner'
    _description = 'Micro Dynamic New Deals Banner'
    _rec_name = 'name'

    deal_banner = fields.Binary(string='Banner')
    name = fields.Char(string='Name')
    show = fields.Boolean(string='Show on Website')