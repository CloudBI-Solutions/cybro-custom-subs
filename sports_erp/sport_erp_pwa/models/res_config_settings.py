import base64
import io
from odoo import modules

from PIL import Image

from odoo import _, api, exceptions, fields, models
from odoo.tools.mimetypes import guess_mimetype


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _pwa_icon_url_base = "/sport_erp_pwa/icon"

    activate_pwa = fields.Boolean(
        string='Activate PWA',
        help='Enable to activate Progressive Web Application')

    pwa_name = fields.Char(
        string='PWA Name',
        default='Sport-ERP',
        help='Sport_ERP Progressive Web Application Name')

    pwa_short_name = fields.Char(
        string='PWA Short Name',
        default='Sport-ERP',
        help='Sport-ERP Progressive Web Application Short Name')

    pwa_description = fields.Char(
        String='PWA Description',
        default='Sport-ERP PWA',
        help='Sport-ERP Progressive Web Application Description')

    pwa_theme_color = fields.Char(
        String='PWA Theme Color',
        default='#ff2905',
        help='Select Your Progressive Web Application Theme Color')

    pwa_background_color = fields.Char(
        String='PWA Background Color',
        default='#feeff0',
        help='Select Your Progressive Web Application Background Color')

    def _get_default_icon(self):
        image_path = modules.get_module_resource('sport_erp_pwa',
                                                 'static/src/img',
                                                 'sport_erp_logo_512.png')
        return base64.b64encode(open(image_path, 'rb').read())

    pwa_icon = fields.Binary(
        String='PWA Icon',
        default=_get_default_icon,
        help='Select The Icon for Progressive Web Application')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_values = self.env["ir.config_parameter"].sudo()
        set_values.set_param('sport_erp_pwa.activate_pwa',
                             self.activate_pwa)
        set_values.set_param("sport_erp_pwa.pwa_name",
                             self.pwa_name)
        set_values.set_param("sport_erp_pwa.pwa_short_name",
                             self.pwa_short_name)
        set_values.set_param('sport_erp_pwa.pwa_description',
                             self.pwa_description)
        set_values.set_param("sport_erp_pwa.pwa_background_color",
                             self.pwa_background_color)
        set_values.set_param("sport_erp_pwa.pwa_theme_color",
                             self.pwa_theme_color)
        pwa_icon_ir_attachments = (
            self.env["ir.attachment"]
            .sudo()
            .search([("url", "like", self._pwa_icon_url_base)])
        )
        decoded_pwa_icon = base64.b64decode(self.pwa_icon)
        pwa_icon_mimetype = guess_mimetype(decoded_pwa_icon)
        pwa_icon_extension = "." + pwa_icon_mimetype.split("/")[-1].split("+")[
            0]
        if not pwa_icon_mimetype.startswith("image/png"):
            raise exceptions.UserError(
                _("Choose PNG File !!!")
            )
        if pwa_icon_ir_attachments:
            pwa_icon_ir_attachments.unlink()
        self._write_icon_to_attachment(pwa_icon_extension, pwa_icon_mimetype)

        if self._unpack_icon(self.pwa_icon).size != (512, 512):
            raise exceptions.UserError(
                _("You can only upload PNG with size 512x512")
            )
        for size in [
            (128, 128),
            (144, 144),
            (152, 152),
            (192, 192),
            (256, 256),
            (512, 512),
        ]:
            self._write_icon_to_attachment(
                pwa_icon_extension, pwa_icon_mimetype, size=size
            )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_values = self.env["ir.config_parameter"].sudo()
        activate_pwa = get_values.get_param('sport_erp_pwa.activate_pwa')
        pwa_name = get_values.get_param(
            "sport_erp_pwa.pwa_name")
        pwa_short_name = get_values.get_param(
            "sport_erp_pwa.pwa_short_name")
        pwa_description = get_values.get_param(
            "sport_erp_pwa.pwa_description")
        pwa_background_color = get_values.get_param(
            "sport_erp_pwa.pwa_background_color")
        pwa_theme_color = get_values.get_param(
            "sport_erp_pwa.pwa_theme_color")
        pwa_icon_ir_attachment = (
            self.env["ir.attachment"]
            .sudo()
            .search([("url", "like", self._pwa_icon_url_base + ".")])
        )
        if activate_pwa:
            res.update(
                activate_pwa=activate_pwa,
                pwa_name=pwa_name,
                pwa_short_name=pwa_short_name,
                pwa_description=pwa_description,
                pwa_theme_color=pwa_theme_color,
                pwa_background_color=pwa_background_color,
                pwa_icon=pwa_icon_ir_attachment.datas if
                pwa_icon_ir_attachment else False
            )
        return res

    def _unpack_icon(self, icon):
        decoded_icon = base64.b64decode(icon)
        icon_bytes = io.BytesIO(decoded_icon)
        return Image.open(icon_bytes)

    def _write_icon_to_attachment(self, extension, mimetype, size=None):
        url = self._pwa_icon_url_base + extension
        icon = self.pwa_icon
        if size:
            image = self._unpack_icon(icon)
            resized_image = image.resize(size)
            icon_bytes_output = io.BytesIO()
            resized_image.save(icon_bytes_output, format=extension.lstrip(
                ".").upper())
            icon = base64.b64encode(icon_bytes_output.getvalue())
            url = "{}{}x{}{}".format(
                self._pwa_icon_url_base,
                str(size[0]),
                str(size[1]),
                extension,
            )
        existing_attachment = (
            self.env["ir.attachment"].sudo().search([("url", "like", url)])
        )
        values = {
            "datas": icon,
            "db_datas": icon,
            "url": url,
            "name": url,
            "type": "binary",
            "mimetype": mimetype,
        }
        if existing_attachment:
            existing_attachment.sudo().write(values)
        else:
            self.env["ir.attachment"].sudo().create(values)
