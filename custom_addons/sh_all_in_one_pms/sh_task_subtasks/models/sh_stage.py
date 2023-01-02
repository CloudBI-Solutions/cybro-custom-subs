# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, api

class TaskStage(models.Model):
    _inherit = "project.task.type"

    sh_done = fields.Boolean("Done")
    sh_cancel = fields.Boolean("Cancel")
    


class SubTask(models.Model):
    _inherit = "project.task"

    sh_sub_task_lines = fields.One2many("project.task", "parent_id",
                                        "Sub Task")

    check_bool_enable_task_sub_task = fields.Boolean(
        related="company_id.enable_task_sub_task")

    subtask_project_id = fields.Many2many("project.task",
                                          compute="_get_subtask_id")

    @api.onchange('stage_id')
    def Onchange(self):
        
        if self.stage_id.sh_done:
            sub_task = self.search([('parent_id', '=', self._origin.id)])
            for rec in sub_task:
                if rec.stage_id.sh_done == False:
                    raise UserError('Complete the sub task first')

        elif self.stage_id.sh_cancel == True:
            sub_task = self.search([('parent_id', '=', self._origin.id)])
            stage_id = self.env['project.task.type'].search(
                [('sh_cancel', '=', True)], limit=1)
            for rec in sub_task:
                rec.sudo().write({'stage_id': stage_id.id})

    def _get_subtask_id(self):
        if self:
            sub_list = []
            for rec in self:
                if rec.sh_sub_task_lines:
                    for lines in rec.sh_sub_task_lines:
                        sub_list.append(lines.id)
            if sub_list:
                self.subtask_project_id = [(6,0,sub_list)]
            else:
                self.subtask_project_id = False

    def action_subtask(self):
        child_ids = self.search([('parent_id','=',self.id)]).ids
        return {
            'name': "Sub Task",
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,form',
            'res_model': 'project.task',
            'target': 'current',
            'domain':[('id','in',child_ids)]
        }
