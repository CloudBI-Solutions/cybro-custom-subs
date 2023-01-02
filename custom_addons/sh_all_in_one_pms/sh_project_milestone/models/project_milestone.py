# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_milestone_manager = fields.Boolean("Milestone Manager ?")


class ProjectMileStone(models.Model):
    _inherit = 'project.milestone'

    state = fields.Selection([('new', 'New'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
                             string="State", default='new', readonly=True, index=True)
    task_count = fields.Integer("Task count", compute='_compute_task_count')

    def _compute_task_count(self):
        if self:
            for data in self:
                data.task_count = data.env['project.task'].search_count(
                    [('milestone_ids', 'in', [data.id])])

    def button_inprogress(self):
        if self:
            for data in self:
                data.write({'state': 'in_progress'})

    def button_completed(self):
        if self:
            for data in self:
                data.write({'state': 'completed'})

    def button_cancelled(self):
        if self:
            for data in self:
                data.write({'state': 'cancelled'})

    def sh_action_milestone_to_task_event(self):
        self.ensure_one()
        return{
            'name':'Milestone To Task',
            'type':'ir.actions.act_window',
            'res_model':'project.task',
            'view_mode':'kanban,tree,form',
            'domain':[('milestone_ids','in',[self.id])],
            'context':{'default_milestone_ids':[(6,0,[self.id])]},
            'target':'current',
        }


class ProjectTask(models.Model):
    _inherit = 'project.task'


    milestone_ids = fields.Many2many('project.milestone', string="Milestone")

    @api.model
    def create(self,vals):
        if vals.get('project_id'):
            project = self.env['project.project'].sudo().browse(vals.get('project_id'))
            if project and project.milestone_ids:
                vals.update({
                    'milestone_ids':[(6,0,project.milestone_ids.ids)]
                })
        return super(ProjectTask,self).create(vals)

    def write(self,vals):
        if vals.get('project_id'):
            project = self.env['project.project'].sudo().browse(vals.get('project_id'))
            if project and project.milestone_ids:
                vals.update({
                    'milestone_ids':[(6,0,project.milestone_ids.ids)]
                })
        return super(ProjectTask,self).write(vals)
