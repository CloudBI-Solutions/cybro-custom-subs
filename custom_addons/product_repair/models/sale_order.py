from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    repair = fields.Boolean(string='Repair', default=False)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        repair_requests = self.env['product.repair'].search([
            ('state', '=', 'confirm')])
        print(repair_requests)
        print(repair_requests.partner_id.ids)
        if self.partner_id.id in repair_requests.partner_id.ids:
            return {
                'warning': {
                    'title': "Warning",
                    'message': "This user has some pending repair request.",
                    },
                }
