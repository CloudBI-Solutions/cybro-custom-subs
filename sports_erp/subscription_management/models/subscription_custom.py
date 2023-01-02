# -*- coding: utf-8 -*-
"""Booking"""

from odoo import fields, models, api, _


class SubscriptionStages(models.Model):
    """ Stages of Booking """
    _name = "subscription.stage"
    _description = "Subscription Stages"
    _rec_name = "name"

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1,
                              help="Used to order stages. Lower is better.")
    description = fields.Text(string='Description', translate=True)
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when '
                               'there are no records in that stage to display.')

    _sql_constraints = [('number_name', 'UNIQUE (name)',
                         'You can not have two stages with the same Name !')]


# class SubscriptionProject(models.Model):
#     _name = "subscription.project"
#     _description = "Subscription Project"
#     _order = "sequence, name, id"
#
#     name = fields.Char("Name", index=True, required=True, tracking=True)
#     sequence = fields.Integer(default=10)
#     tasks = fields.One2many('subscription.tasks', 'sub_project_id', string="Task Activities")
#     sub_plan_id = fields.Many2one('subscription.plan',  string="Subscription Plan", required=True)
#
#     def action_view_tasks(self):
#         action = self.with_context(active_id=self.id, active_ids=self.ids) \
#             .env.ref('subscription_management.act_project_project_2_project_task_all') \
#             .sudo().read()[0]
#         action['display_name'] = self.name
#         return action

# class SubscriptionTasks(models.Model):
#     """ Subscription Tasks """
#     _name = "subscription.tasks"
#     _description = "Subscription Tasks"
#     _order = "sequence desc"
#
#     name = fields.Char('Stage Name', required=True, translate=True)
#     sequence = fields.Integer('Sequence', help="Used to order tasks.")
#     task_type_selection = fields.Selection(
#         [('admin', 'Administrative'), ('plan', 'Planning')],
#         string="Task type", tracking=True, default='admin', required=True)
#     assign_type_selection = fields.Selection(
#         [('athlete', 'Athlete'), ('group', 'Group'), ('coach', 'Coach')],
#         string="Assign to", tracking=True)
#     sub_plan_id = fields.Many2one('subscription.plan',  string="Subscription Plan", required=True)
#     stage_id = fields.Many2one('project.task.type', string='Task stage')
#
#     assign_athlete_ids = fields.One2many('organisation.athletes', 'sub_task_id', string="Athletes")
#     assign_group_ids = fields.One2many('athlete.groups',  'sub_task_id', string="Groups")
#     assign_coach_ids = fields.One2many('organisation.coaches', 'sub_task_id', string="Coaches")
#
#     user_id = fields.Many2one('res.users', string='Assigned to', index=True,
#                               tracking=True, default=False)
#     venue_id = fields.Many2one('organisation.venues', string="Venue", tracking=True)
#     start_datetime = fields.Datetime(string="Starting from", tracking=True)
#     task_event_duration = fields.Float(string="Duration", default=0, tracking=True)
#     calendar_event_id = fields.Many2one('calendar.event', string="Event")
#     task_checkbox = fields.Boolean(string="Task Checkbox", default=False)
#
#     sub_project_id = fields.Many2one('subscription.project', string='Subscription Project',
#                                      store=True, readonly=False, index=True, tracking=True, check_company=True,
#                                      change_default=True)
#
#     task_mode = fields.Selection(
#         [('session', 'Session'), ('one2one', 'One to One'), ('other', 'Other')],
#         string="Task Mode", default='session', required=True)
#
#     description = fields.Text(string='Description', translate=True)

# class Athletes(models.Model):
#     _inherit = "organisation.athletes"
#
#     sub_task_id = fields.Many2one('subscription.tasks', string="Subscription Tasks")
#
#
# class AthleteGroups(models.Model):
#     _inherit = "athlete.groups"
#
#     sub_task_id = fields.Many2one('subscription.tasks', string="Subscription Tasks")
#
#
# class Coaches(models.Model):
#     _inherit = "organisation.coaches"
#
#     sub_task_id = fields.Many2one('subscription.tasks', string="Subscription Tasks")
