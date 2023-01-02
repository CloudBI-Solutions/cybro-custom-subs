from odoo import models, fields, api


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    time_off_approver_ids = fields.Many2many('res.users')


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    time_off_approver_ids = fields.Many2many(
        'res.users',
        related='holiday_status_id.time_off_approver_ids',
        readonly=True)



