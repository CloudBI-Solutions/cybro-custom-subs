from odoo import api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    sub_plan_id = fields.Many2one('subscription.plan',
                                  string="Subscription Plan")
    is_template = fields.Boolean(string="Project Template", default=False)
    subscription_id = fields.Many2one('subscription.subscription', copy=False,
                                      string="Subscription", store=True)


class Task(models.Model):
    _inherit = 'project.task'

    session_planned_date = fields.Date(string="Planned Date", copy=False)
    is_session = fields.Boolean(string="Is Session", default=False, copy=False,
                                readonly=True)
    is_o2o = fields.Boolean(string="Is One to One", default=False, copy=False,
                            readonly=True)
    is_booked = fields.Boolean(string="Is Booked", default=False, copy=False,
                               readonly=True, compute='_compute_is_booked',
                               store=True)
    is_used = fields.Boolean(string="Is Used", default=False, copy=False,
                             readonly=True, compute='_compute_is_used')

    @api.depends('session_planned_date')
    def _compute_is_booked(self):
        for task in self:
            task.is_booked = False
            if task.session_planned_date:
                task.is_booked = True

    # @api.depends('session_planned_date')
    def _compute_is_used(self):
        for task in self:
            task.is_used = False
            employee = False
            # if task.session_planned_date:
            #     task.is_booked = True
            partner = task.project_id.partner_id
            if task.is_booked:
                org_category = partner.org_group_selection
                if org_category == "athletes":
                    athlete = self.env['organisation.athletes'].sudo().search([
                        ('partner_id', '=', partner.id)])
                    employee = athlete.employee_id
                elif org_category == "ex_coaches":
                    coach = self.env['organisation.coaches'].sudo().search([
                        ('partner_id', '=', partner.id)])
                    employee = coach.employee_id
                else:
                    pass
                if employee.id:
                    checkin = self.env['hr.attendance'].sudo().search([
                        ('employee_id', '=', employee.id)
                    ])
                    if checkin:
                        task.is_used = True
