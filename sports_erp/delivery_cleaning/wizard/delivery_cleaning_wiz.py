from odoo import models, fields


class DeliveryCleaning(models.TransientModel):
    _name = 'delivery.cleaning.wizard'

    delivery_id = fields.Many2one(
        'stock.picking', string='Delivery Orders',
        domain="[('picking_type_code', '=',  'outgoing')]")

    def action_clean(self):
        if self.delivery_id:
            delivery_order = self.delivery_id
            if delivery_order.state == 'done':
                print(delivery_order)

