from odoo import models, fields, api


class ProductRepair(models.Model):
    _name = 'product.repair'
    _inherit = 'mail.thread'
    _description = 'Product Repair'

    name = fields.Char(string="Request Number", readonly=True,
                       copy=False, default='Draft')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'product.repair')
        return super(ProductRepair, self).create(vals)

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    product_id = fields.Many2one('product.product', string='Product')
    partner_id = fields.Many2one('res.partner', save=True)

    @api.onchange('sale_order_id')
    def on_change_sale_order_id(self):
        # record = self.env['res.partner'].search([])
        # print(record.name)
        self.partner_id = False
        self.partner_id = self.sale_order_id.partner_id.id
        self.product_id = False
        return {'domain': {'product_id': [('id',
                                           '=',
                                           self.sale_order_id.order_line.
                                           product_id.ids)]}}

    def button_confirm(self):
        print("state", self.sale_order_id.repair)
        self.state = "confirm"
        self.sale_order_id.repair = True
        print("state", self.sale_order_id.repair)
        print(self.state)

    def button_done(self):
        print("button", self)
        self.state = "done"
        # print(self.test)
        print(self.state)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done')],
        string='Status',
        required=True,
        copy=False,
        default='draft',
        track_visibility='onchange')
