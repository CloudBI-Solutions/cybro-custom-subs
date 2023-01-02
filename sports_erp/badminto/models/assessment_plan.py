from odoo import models, fields, api


class BadmintoAssessmentPlan(models.Model):
    _name = 'assessment.plan'
    _description = "Badminto Assessment Plan"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    assessment_type_ids = fields.Many2many('assessment.types')

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                 self: self.env.user.company_id.id)

    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                  self: self.env.user.company_id.currency_id.id)

    price = fields.Monetary(string="Price")

    tax_ids = fields.Many2many('account.tax')
    sequence_format = fields.Char()
    product_id = fields.Many2one('product.product')
    organisation_id = fields.Many2one('organisation.organisation')

    @api.model
    def create(self, vals):
        res = super(BadmintoAssessmentPlan, self).create(vals)
        for rec in res:
            product_id = self.env['product.product'].sudo().create({
                'name': rec.name,
                'list_price': rec.price,
                'currency_id': self.env.company.currency_id.id,
                'detailed_type': 'service',
                'is_badminto_product': True,
                'taxes_id': self.tax_ids.ids,
                'organisation_ids': [(4, rec.organisation_id.id)]
                if rec.organisation_id else False,
            })
            rec['product_id'] = product_id.id
        return res

    def get_badminto_product(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Badminto Product',
            'view_mode': 'form',
            'res_model': 'product.product',
            'res_id': self.product_id.id,
        }


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_badminto_product = fields.Boolean(
        string='Is Badmintoo Product')
