# -*- coding: utf-8 -*-
from odoo import models, fields


class IrAttachmentInherit(models.Model):
    _inherit = 'ir.attachment'

    web_video_file_data = fields.Text()



class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    web_video_file = fields.Binary()

    def upload_video_adds(self, rec_id, file, name):
        self.env['ir.attachment'].create({
            'name': name,
            'web_video_file_data': file,
            'res_model': 'product.template',
            'res_id': rec_id
        })

    def load_video_adds(self, rec_id):
        res = self.env['ir.attachment'].search(
            [('res_id', '=', rec_id), ('mimetype', '=', 'video/mp4'),
             ('res_model', '=', 'product.template')])
        data = {}
        if res:
            data = {
                'name': res['name'],
                'datas': res['web_video_file_data']
            }
        return data

    def update_video_adds(self, rec_id):
        self.env['ir.attachment'].search([('res_id', '=', rec_id),
                                          ('mimetype', '=', 'video/mp4'),
                                          ('res_model', '=',
                                           'product.template')]).unlink()
