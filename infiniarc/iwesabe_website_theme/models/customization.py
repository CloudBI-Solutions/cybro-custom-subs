from odoo import fields, models, api, _

try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO
from odoo.exceptions import UserError


class ManufacturingOrder(models.Model):
    _inherit = 'mrp.production'

    is_customize = fields.Boolean()