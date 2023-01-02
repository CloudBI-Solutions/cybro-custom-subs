import base64
from odoo import fields, models, api, modules


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pwa_enable = fields.Boolean(string='Enable PWA',
                                default=False)
    pwa_name = fields.Char(string='PWA Name',
                           default='Odoo PWA')
    pwa_short_name = fields.Char(string='PWA Name',
                                 default='Odoo PWA')
    pwa_description = fields.Char(string='PWA Name',
                                  default='Odoo PWA')
    pwa_theme_color = fields.Char(string='PWA Name',
                                  default='#7C7BAD')
    pwa_background_color = fields.Char(string='PWA Name',
                                       default='#AE008A')
    pwa_start_link = fields.Char(string='Start PWA from',
                                 default='/')

    def get_icon_pwa(self):
        image_path = modules.get_module_resource('base_pwa',
                                                 'static/src/img',
                                                 'default_icon_512x512.png')
        return base64.b64encode(open(image_path, 'rb').read())

    pwa_icon = fields.Binary(string='PWA Icon', default=get_icon_pwa)

    pwa_icon_link = fields.Char(string='Odoo link')

    # @api.onchange('pwa_icon')
    # def onchange_pwa(self):
    #     real_attachment = self.env['ir.attachment'].create({
    #         'name': 'PWA_Icon',
    #         'type': 'binary',
    #         'datas': self.pwa_icon
    #     })
    #     for rec in self.env['ir.attachment'].search([
    #             ('res_field', '!=', 'pwa_icon'),
    #             ('id', '!=', real_attachment.id),
    #             ('name', 'ilike', 'PWA_Icon')
    #             ]):
    #         rec.unlink()
    #     self.pwa_icon_link = self.get_base_url() + \
    #                          '/web/content/' +\
    #                          str(real_attachment.id)
    #     print(self.pwa_icon_link)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_values = self.env["ir.config_parameter"].sudo()
        set_values.set_param('base_pwa.pwa_enable',
                             self.pwa_enable)
        set_values.set_param("base_pwa.pwa_name",
                             self.pwa_name)
        set_values.set_param("base_pwa.pwa_short_name",
                             self.pwa_short_name)
        set_values.set_param('base_pwa.pwa_description',
                             self.pwa_description)
        set_values.set_param("base_pwa.pwa_background_color",
                             self.pwa_background_color)
        set_values.set_param("base_pwa.pwa_theme_color",
                             self.pwa_theme_color)
        set_values.set_param("base_pwa.pwa_start_link",
                             self.pwa_start_link)
        set_values.set_param("base_pwa.pwa_icon",
                             self.pwa_icon)
        set_values.set_param("base_pwa.pwa_icon_link",
                             self.pwa_icon_link)
        real_attachment = self.env['ir.attachment'].create({
            'name': 'PWA_Icon',
            'type': 'binary',
            'datas': self.pwa_icon
        })
        for rec in self.env['ir.attachment'].search([
                ('id', '!=', real_attachment.id),
                ('name', 'ilike', 'PWA_Icon')
                ]):
            rec.unlink()
        self.pwa_icon_link = self.get_base_url() + \
                             '/web/content/' +\
                             str(real_attachment.id)
        print("self", self.pwa_icon_link)


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_values = self.env["ir.config_parameter"].sudo()
        pwa_enable = get_values.get_param('base_pwa.pwa_enable')
        pwa_name = get_values.get_param(
            "base_pwa.pwa_name")
        pwa_short_name = get_values.get_param(
            "base_pwa.pwa_short_name")
        pwa_description = get_values.get_param(
            "base_pwa.pwa_description")
        pwa_background_color = get_values.get_param(
            "base_pwa.pwa_background_color")
        pwa_theme_color = get_values.get_param(
            "base_pwa.pwa_theme_color")
        pwa_start_link = get_values.get_param(
            "base_pwa.pwa_start_link")
        pwa_icon = get_values.get_param(
            "base_pwa.pwa_icon")
        pwa_icon_link = get_values.get_param(
            "base_pwa.pwa_icon_link")
        if pwa_enable:
            res.update(
                pwa_enable=pwa_enable,
                pwa_name=pwa_name,
                pwa_short_name=pwa_short_name,
                pwa_description=pwa_description,
                pwa_theme_color=pwa_theme_color,
                pwa_background_color=pwa_background_color,
                pwa_start_link=pwa_start_link,
                pwa_icon=pwa_icon,
                pwa_icon_link=pwa_icon_link
            )
            print('get_values')
        return res

