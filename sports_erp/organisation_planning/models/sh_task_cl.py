from odoo import fields, models, api


class TaskChecklist(models.Model):
    _inherit = "task.checklist"

    state = fields.Selection([('new', 'New'), ('completed', 'Completed')],
                             string="State",
                             default='new',
                             readonly=True,
                             index=True)
    athlete_id = fields.Many2one('organisation.athletes', string="Athlete")
    coach_id = fields.Many2one('organisation.coaches', string="Coach")
    group_id = fields.Many2one('athlete.groups', string="Group")
    task_id = fields.Many2one('project.task', string="Task")

    def btn_check(self):
        for rec in self:
            rec.write({'state': 'completed'})


class ProjectTask(models.Model):
    _inherit = 'project.task'

    checklist_ids = fields.Many2many("task.checklist", 'checklist_task_rel',
                                     'task_id', 'checklist_id',
                                     string="Checklist")
    checklist = fields.Float("Checklist Completed",
                             compute="_compute_checklist")

    @api.depends('checklist_ids')
    def _compute_checklist(self):
        for rec in self:
            total_cnt = len(rec.checklist_ids)
            if total_cnt:
                checked = rec.checklist_ids.search([(
                    'state', '=', 'completed'
                )])
                checked_cnt = len(checked)
                if checked_cnt == 0:
                    rec.checklist = 0
                else:
                    rec.checklist = (100.0 * checked_cnt) / total_cnt
            else:
                rec.checklist = 0

#
# class Athletes(models.Model):
#     """model for managing athletes"""
#     _inherit = "organisation.athletes"
#
#     @api.model
#     def create(self, vals_list):
#         result = super(Athletes, self).create(vals_list)
#         vals = {
#             'name': result.partner_id.name,
#             'state': 'new',
#             'athlete_id': result.id,
#         }
#         self.env['task.checklist'].create(vals)
#         return result
#
#
# class Coaches(models.Model):
#     """model for managing coaches"""
#     _inherit = "organisation.coaches"
#
#     @api.model
#     def create(self, vals_list):
#         result = super(Coaches, self).create(vals_list)
#         vals = {
#             'name': result.partner_id.name,
#             'state': 'new',
#             'coach_id': result.id,
#         }
#         self.env['task.checklist'].create(vals)
#         return result
#
#
# class AthleteGroups(models.Model):
#     """model for managing athletes"""
#     _inherit = "athlete.groups"
#
#     @api.model
#     def create(self, vals_list):
#         result = super(AthleteGroups, self).create(vals_list)
#         vals = {
#             'name': result.partner_id.name,
#             'state': 'new',
#             'group_id': result.id,
#         }
#         self.env['task.checklist'].create(vals)
#         return result

