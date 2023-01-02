
from odoo import models, fields, api, SUPERUSER_ID, _
from datetime import timedelta
from odoo.exceptions import ValidationError

from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU
DAYS = {
    'mon': MO,
    'tue': TU,
    'wed': WE,
    'thu': TH,
    'fri': FR,
    'sat': SA,
    'sun': SU,
}

WEEKS = {
    'first': 1,
    'second': 2,
    'third': 3,
    'last': 4,
}


class Event(models.Model):
    _inherit = "calendar.event"

    org_planning_id = fields.Many2one('project.task', string="Task",
                                      readonly=True)


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    task_type_selection = fields.Selection(
        [('admin', 'Administrative'), ('plan', 'Planning')],
        string="Task type", tracking=True)


class Project(models.Model):
    _inherit = "project.project"

    is_training = fields.Boolean("Training", default=True,
                                 help="Display Projects and tasks in the "
                                      "Organisation planning module")
    org_task_count = fields.Integer(compute='_compute_org_task_count',
                                    string="Planning Task Count")
    adm_task_count = fields.Integer(compute='_compute_adm_task_count',
                                    string="Administrative Task Count")

    def _compute_org_task_count(self):
        task_data = self.env['project.task'].read_group(
            [('project_id', 'in', self.ids), ('is_training', '=', True),
             ('task_type_selection', '=', 'plan'),
             '|', '&', ('stage_id.is_closed', '=', False),
             ('stage_id.fold', '=', False), ('stage_id', '=', False)],
            ['project_id'], ['project_id'])
        result = dict((data['project_id'][0], data['project_id_count'])
                      for data in task_data)
        for project in self:
            project.org_task_count = result.get(project.id, 0)

    def _compute_adm_task_count(self):
        task_data = self.env['project.task'].read_group(
            [('project_id', 'in', self.ids),
             ('task_type_selection', '=', 'admin'),
             '|', '&', ('stage_id.is_closed', '=', False),
             ('stage_id.fold', '=', False), ('stage_id', '=', False)],
            ['project_id'], ['project_id'])
        result = dict((data['project_id'][0], data['project_id_count'])
                      for data in task_data)
        for project in self:
            project.adm_task_count = result.get(project.id, 0)

    def org_action_view_tasks(self):
        form_view_ref = self.env.ref('organisation_planning.org_view_task_form2', False)
        tree_view_ref = self.env.ref('organisation_planning.org_view_task_tree2', False)
        kanban_view_ref = self.env.ref('organisation_planning.org_view_task_kanban', False)
        return {
            'name': "Tasks",
            'type': 'ir.actions.act_window',
            'view_id': False,
            'res_model': 'project.task',
            'view_mode': 'kanban,tree,form,calendar,pivot,graph,activity',
            'views': [(kanban_view_ref.id, 'kanban'), (tree_view_ref.id, 'tree'), (form_view_ref.id, 'form')],
            'domain': [('project_id', '=', self.id),
                       ('task_type_selection', '=', 'plan')],
            'context': {'default_project_id': self.id},
            'target': 'current'
        }

    def view_project_project_2_project_task_all(self):
        form_view_ref = self.env.ref('organisation_planning.org_view_task_form2', False)
        tree_view_ref = self.env.ref('organisation_planning.org_view_task_tree2', False)
        kanban_view_ref = self.env.ref('organisation_planning.org_view_task_kanban', False)
        return {
            'name': "Tasks",
            'type': 'ir.actions.act_window',
            'view_id': False,
            'res_model': 'project.task',
            'view_mode': 'kanban,tree,form,calendar,pivot,graph,activity',
            'views': [(kanban_view_ref.id, 'kanban'), (tree_view_ref.id, 'tree'), (form_view_ref.id, 'form')],
            'domain': [('project_id', '=', self.id),
                       ('task_type_selection', '=', 'plan')],
            'context': {'create': False, 'default_project_id': self.id},
            'target': 'current'
        }


class Task(models.Model):
    _inherit = "project.task"

    def _get_default_org_stage_id(self):
        """ Gives default org stage_id """
        project_id = self.env.context.get('default_project_id')
        if not project_id:
            return False
        return self.stage_find(project_id, [('task_type_selection', '=', 'plan'),
                                            ('fold', '=', False), ('is_closed', '=', False)])

    is_mail_send = fields.Boolean(string="Is mail send", default=False,
                                  copy=False, store=True)
    user_id = fields.Many2one('res.users', string='Assigned to', index=True,
                              tracking=True, default=False)
    is_training = fields.Boolean("Training", related='project_id.is_training',
                                 readonly=False, default=True)
    task_type_selection = fields.Selection(
        [('admin', 'Administrative'), ('plan', 'Planning')],
        string="Task type", tracking=True, default='admin', required=True)
    assign_type_selection = fields.Selection(
        [('athlete', 'Athlete'), ('group', 'Group'), ('coach', 'Coach')],
        string="Assign to", tracking=True)
    assign_athlete_ids = fields.Many2many(
        'organisation.athletes', 'task_athlete_rel', 'task_id', 'athlete_id',
        string="Athletes", tracking=True)
    assign_group_ids = fields.Many2many(
        'athlete.groups', 'task_group_rel', 'task_id', 'group_id',
        string="Groups", tracking=True)
    assign_coach_ids = fields.Many2many(
        'organisation.coaches', 'task_coach_rel', 'task_id', 'coach_id',
        string="Coaches", tracking=True)
    venue_id = fields.Many2one('organisation.venues', string="Venue", tracking=True)
    start_datetime = fields.Datetime(string="Starting from", tracking=True)
    task_event_duration = fields.Float(string="Duration", default=0, tracking=True)
    calendar_event_id = fields.Many2one('calendar.event', string="Event")
    task_checkbox = fields.Boolean(string="Task Checkbox", default=False)
    org_stage_id = fields.Many2one(
        'project.task.type', string='Stage', compute='_compute_org_stage_id',
        store=True, readonly=False, ondelete='restrict', tracking=True, index=True,
        default=_get_default_org_stage_id, group_expand='_read_group_org_stage_ids',
        domain="[('project_ids', '=', project_id), ('task_type_selection', '=', 'plan')]",
        copy=False)

    @api.onchange('task_type_selection')
    def _onchange_task_type_selection(self):
        if self.task_type_selection == 'admin':
            self.assign_type_selection = False
            self.assign_group_ids = False
            self.assign_coach_ids = False
            self.assign_athlete_ids = False

    @api.onchange('assign_type_selection')
    def _onchange_assign_type_selection(self):
        if self.assign_type_selection == 'athlete':
            self.assign_group_ids = False
            self.assign_coach_ids = False
        if self.assign_type_selection == 'group':
            self.assign_coach_ids = False
            self.assign_athlete_ids = False
        if self.assign_type_selection == 'coach':
            self.assign_group_ids = False
            self.assign_athlete_ids = False

    @api.depends('project_id')
    def _compute_org_stage_id(self):
        for task in self:
            if task.project_id:
                if task.project_id not in task.org_stage_id.project_ids:
                    task.org_stage_id = task.stage_find(task.project_id.id, [
                        ('task_type_selection', '=', 'plan'), ('fold', '=', False), ('is_closed', '=', False)])
            else:
                task.org_stage_id = False

    @api.model
    def _read_group_org_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids), ('task_type_selection', '=', 'plan')]
        if 'default_project_id' in self.env.context:
            search_domain = ['|', ('project_ids', '=', self.env.context['default_project_id'])] + search_domain

            stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
            return stages.browse(stage_ids)

    def action_send_mail(self):
        if not self.calendar_event_id:
            raise ValidationError("No related event found!!")
        self.is_mail_send = True
        template_id = self.env.ref(
            'calendar.calendar_template_meeting_invitation').id
        template = self.env['mail.template'].sudo().browse(template_id)
        print(self, self.calendar_event_id.id, self.calendar_event_id.attendee_ids)
        attendees = self.calendar_event_id.attendee_ids
        for attendee in attendees:
            template.sudo().send_mail(attendee.id, force_send=True)

    def action_create_event(self):
        if not self.task_event_duration or not self.start_datetime:
            raise ValidationError("Start date / Duration is missing!!")
        vals = {}
        if self.recurring_task:
            vals.update({
                'recurrency': True,
                'interval': self.repeat_interval,
            })
            if self.repeat_unit == 'day':
                vals.update({
                    'rrule_type': 'daily',
                })
            elif self.repeat_unit == 'week':
                vals.update({
                    'mo': self.mon,
                    'tu': self.tue,
                    'we': self.wed,
                    'th': self.thu,
                    'fr': self.fri,
                    'sa': self.sat,
                    'su': self.sun,
                    'rrule_type': 'weekly',
                })
            elif self.repeat_unit == 'month':
                vals.update({
                    'rrule_type': 'monthly',
                })
                if self.repeat_on_month == 'date':
                    vals.update({
                        'month_by': 'date',
                        'day': int(self.repeat_day)
                    })
                elif self.repeat_on_month == 'day':
                    vals.update({
                        'month_by': 'day',
                    })
                    if self.repeat_week == 'first':
                        vals.update({
                            'byday': '1',
                        })
                    elif self.repeat_week == 'second':
                        vals.update({
                            'byday': '2',
                        })
                    elif self.repeat_week == 'third':
                        vals.update({
                            'byday': '3',
                        })
                    elif self.repeat_week == 'last':
                        vals.update({
                            'byday': '-1',
                        })
                    else:
                        pass
                    if self.repeat_weekday == 'mon':
                        vals.update({
                            'weekday': 'MO',
                        })
                    elif self.repeat_weekday == 'tue':
                        vals.update({
                            'weekday': 'TU',
                        })
                    elif self.repeat_weekday == 'wed':
                        vals.update({
                            'weekday': 'WE',
                        })
                    elif self.repeat_weekday == 'thu':
                        vals.update({
                            'weekday': 'TH',
                        })
                    elif self.repeat_weekday == 'fri':
                        vals.update({
                            'weekday': 'FR',
                        })
                    elif self.repeat_weekday == 'sat':
                        vals.update({
                            'weekday': 'SA',
                        })
                    elif self.repeat_weekday == 'sun':
                        vals.update({
                            'weekday': 'SU',
                        })
                else:
                    pass
            elif self.repeat_unit == 'year':
                vals.update({
                    'rrule_type': 'yearly'
                })
            else:
                pass
            if self.repeat_type == 'after':
                vals.update({
                    'end_type': 'count',
                    'count': self.repeat_number + 1
                })
            elif self.repeat_type == 'forever':
                vals.update({
                    'end_type': 'forever',
                })
            elif self.repeat_type == 'until':
                vals.update({
                    'end_type': 'end_date',
                    'until': self.repeat_until
                })
            else:
                pass
        if self.assign_type_selection == 'athlete':
            partners = self.assign_athlete_ids
            stop = self.start_datetime + timedelta(
                minutes=round((self.task_event_duration or 1.0) * 60))
            vals.update({
                'name': self.name,
                'start': self.start_datetime,
                'stop': stop,
                'duration': self.task_event_duration,
                'org_planning_id': self.id
            })
            event = self.env['calendar.event'].create(vals)
            events = event.recurrence_id.calendar_event_ids
            for event in events:
                event.partner_ids = partners.partner_id
            self.calendar_event_id = event.id
            event.partner_ids = partners.partner_id
        elif self.assign_type_selection == 'coach':
            partners = self.assign_coach_ids
            stop = self.start_datetime + timedelta(
                minutes=round((self.task_event_duration or 1.0) * 60))
            vals.update({
                'name': self.name,
                'start': self.start_datetime,
                'stop': stop,
                'duration': self.task_event_duration,
                'org_planning_id': self.id
            })
            event = self.env['calendar.event'].create(vals)
            self.calendar_event_id = event.id
            event.partner_ids = partners.partner_id
        elif self.assign_type_selection == 'group':
            partners = self.assign_group_ids.athlete_ids
            stop = self.start_datetime + timedelta(
                minutes=round((self.task_event_duration or 1.0) * 60))
            vals.update({
                'name': self.name,
                'start': self.start_datetime,
                'stop': stop,
                'duration': self.task_event_duration,
                'org_planning_id': self.id
            })
            event = self.env['calendar.event'].create(vals)
            self.calendar_event_id = event.id
            event.partner_ids = partners.partner_id
        else:
            stop = self.start_datetime + timedelta(
                minutes=round((self.task_event_duration or 1.0) * 60))
            vals.update({
                'name': self.name,
                'start': self.start_datetime,
                'stop': stop,
                'duration': self.task_event_duration,
                'org_planning_id': self.id
            })
            event = self.env['calendar.event'].create(vals)
            self.calendar_event_id = event.id

    @api.depends(
        'recurring_task', 'repeat_interval', 'repeat_unit', 'repeat_type',
        'repeat_until',
        'repeat_number', 'repeat_on_month', 'repeat_on_year', 'mon', 'tue',
        'wed', 'thu', 'fri',
        'sat', 'sun', 'repeat_day', 'repeat_week', 'repeat_month',
        'repeat_weekday', 'start_datetime')
    def _compute_recurrence_message(self):
        self.recurrence_message = False
        for task in self.filtered(
                lambda t: t.recurring_task and t._is_recurrence_valid()):
            date = fields.Date.today()
            if task.start_datetime:
                date = task.start_datetime
            number_occurrences = min(5,
                                     task.repeat_number if task.repeat_type == 'after' else 5)
            delta = task.repeat_interval if task.repeat_unit == 'day' else 1
            recurring_dates = self.env[
                'project.task.recurrence']._get_next_recurring_dates(
                date + timedelta(days=delta),
                task.repeat_interval,
                task.repeat_unit,
                task.repeat_type,
                task.repeat_until,
                task.repeat_on_month,
                task.repeat_on_year,
                task._get_weekdays(WEEKS.get(task.repeat_week)),
                task.repeat_day,
                task.repeat_week,
                task.repeat_month,
                count=number_occurrences)
            date_format = self.env['res.lang']._lang_get(
                self.env.user.lang).date_format
            task.recurrence_message = '<ul>'
            for date in recurring_dates[:5]:
                task.recurrence_message += '<li>%s</li>' % date.strftime(
                    date_format)
            if task.repeat_type == 'after' and task.repeat_number > 5 or task.repeat_type == 'forever' or len(
                    recurring_dates) > 5:
                task.recurrence_message += '<li>...</li>'
            task.recurrence_message += '</ul>'
            if task.repeat_type == 'until':
                task.recurrence_message += _(
                    '<p><em>Number of tasks: %(tasks_count)s</em></p>') % {
                                               'tasks_count': len(
                                                   recurring_dates)}

    @api.model
    def create(self, vals):
        result = super(Task, self).create(vals)
        o_checklists = self.env['task.checklist'].search(
            [('task_id', '=', self.id)])
        o_checklists.sudo().unlink()
        if result.assign_type_selection == 'athlete':
            athletes = result.assign_athlete_ids
            for athlete in athletes:
                new_checklist_vals = {
                    'name': athlete.name,
                    'state': 'new',
                    'athlete_id': athlete.id,
                    'task_id': result.id
                }
                self.env['task.checklist'].create(new_checklist_vals)
            checklists = self.env['task.checklist'].search(
                [('task_id', '=', result.id)])
            result.checklist_ids = checklists
        elif result.assign_type_selection == 'coach':
            coaches = result.assign_coach_ids
            for coach in coaches:
                new_checklist_vals = {
                    'name': coach.name,
                    'state': 'new',
                    'coach_id': coach.id,
                    'task_id': result.id
                }
                self.env['task.checklist'].create(new_checklist_vals)
            checklists = self.env['task.checklist'].search(
                [('task_id', '=', result.id)])
            result.checklist_ids = checklists
        elif result.assign_type_selection == 'group':
            groups = result.assign_group_ids
            for group in groups:
                new_checklist_vals = {
                    'name': group.name,
                    'state': 'new',
                    'group_id': group.id,
                    'task_id': result.id
                }
                self.env['task.checklist'].create(new_checklist_vals)
            checklists = self.env['task.checklist'].search(
                [('task_id', '=', result.id)])
            result.checklist_ids = checklists
        return result
