from odoo import fields, models, api, _


class BookingProduct(models.Model):
    _inherit = 'product.template'

    is_booking = fields.Boolean('Is Booking Product')


class BookingProduct(models.Model):
    _inherit = 'product.product'

    is_booking = fields.Boolean('Is Booking Product')
    booking_type_id = fields.Many2one('booking.type')

    @api.onchange('is_booking')
    def _onchange_is_booking(self):
        if self.is_booking:
            self.detailed_type = 'service'

    @api.depends('list_price', 'price_extra')
    def _compute_product_lst_price(self):
        res = super(BookingProduct, self)._compute_product_lst_price()
        for product in self:
            override = product.booking_type_id.override_product_price
            if override and product.is_booking and product.booking_type_id:
                list_price = product.booking_type_id.coach_id.price_o2o if product.booking_type_id.session_type == 'one2one' else product.booking_type_id.coach_id.price_team
                product.lst_price = list_price + product.price_extra
        return res
