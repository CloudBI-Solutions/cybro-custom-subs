# -*- coding: utf-8 -*-

from odoo import models, fields


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    upload_date = fields.Date(string="Upload Date")
    reference = fields.Char(string="Reference")
