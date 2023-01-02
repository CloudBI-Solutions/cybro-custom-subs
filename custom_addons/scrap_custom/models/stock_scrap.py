from odoo import fields, models, api


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    @api.onchange('product_id')
    def onchange_product_id(self):
        # test = self.mapped('id')
        # print('test', test)
        print(self.product_id)
        print(self.location_id)
        putaway_location = self.env['stock.putaway.rule'].search([
            ('product_id', '=', self.product_id.id)
        ], limit=1)
        print(putaway_location.location_out_id.id)
        self.location_id = putaway_location.location_out_id.id
