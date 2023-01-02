from odoo import models, fields, api


class EmployeeHelpdesk(models.Model):
    _name = 'employee.helpdesk'
    _inherit = 'mail.thread'
    _description = 'Employee Helpdesk'
    _order = 'name'

    name = fields.Char(string='Title', required=True,
                       readonly=True,
                       copy=False, default='Draft')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'employee.helpdesk')
        return super(EmployeeHelpdesk, self).create(vals)

    employee_id = fields.Many2one('res.users', required='True', string='User')
    subject = fields.Text(string='Subject')
