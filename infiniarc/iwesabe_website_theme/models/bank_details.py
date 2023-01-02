from odoo import api, models, fields


class CompanyBanks(models.Model):
    _name = "company.banks"
    _description = 'Company Banks'

    name = fields.Char(string='Bank Name', required=True)
    bank_image = fields.Binary(string='Photo')
    name_in_ac = fields.Char(string='Account Name')
    account_no = fields.Char(string='A/C Number', required=True)
    parent_id = fields.Many2one('res.company', string='Parent Company', default=lambda self: self.env.company)
    email = fields.Char(related='parent_id.email', store=True, readonly=False)
    mobile = fields.Char('Outlet Mobile no:', store=True, readonly=False)
    text = fields.Html(string='Description', readonly=True)
