from odoo import api, models, fields, _


class ProductTemplateInheritView(models.Model):
    _inherit = "product.template"

    memory_type = fields.Many2one('memories.type', string='Memory Type')

    # socket_type =

    # def _get_filter_type(self):
    #
    #     fiter_type = self.env.ref("iwesabe_website_theme.data_product_filters")
    #     try:
    #         if self.env.context['default_gaming_pc'] == True:
    #             return fiter_type.id
    #         return False
    #     except:
    #         return False

    filter_type = fields.Many2one('product.filter', string='PC Type')
    # filter_type = fields.Many2one('product.filter', string='PC Type', default=_get_filter_type)
    model_ids = fields.Many2one('product.model', string='Product Model')
    gpu_id = fields.Many2one('gpu.gpu', string='GPU')

    # def get_pc(self):
    #     fitertype = self.env['product.filter'].search([('name','=', 'gaming pc')])


class SocketType(models.Model):
    _name = 'socket.type'

    name = fields.Char(string='Name')
    cpu_type = fields.Many2one("cpu.type", string="CPU Type")
