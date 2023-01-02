from odoo import fields, models, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    limit_discount_check = fields.Boolean(default=False,
                                          string='Limit Discount')
    company_currency_id = fields.Many2one('res.currency',
                                          related='company_id.currency_id')
    limit_discount = fields.Monetary(string="Discount Amount",
                                     currency_field='company_currency_id',
                                     readonly=False)

    @api.constrains('limit_discount_check')
    def discount_check(self):
        if not self.limit_discount_check:
            self.limit_discount = 0
        print(self.limit_discount_check)
        print(self.limit_discount)
