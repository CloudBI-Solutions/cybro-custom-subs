from odoo import models


class SaasPricing(models.Model):
    _name = 'saas.pricing'

    def get_depend_module(self):
        module = self.env['ir.module.module'].browse(int(self.id))
        depend_module = module.dependencies_id.depend_id.filtered(
            lambda r: r.application)
        print(depend_module.mapped('shortdesc'))
        return depend_module.ids
