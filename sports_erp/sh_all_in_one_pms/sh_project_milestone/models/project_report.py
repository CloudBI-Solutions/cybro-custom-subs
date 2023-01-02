# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"

    milestone_id = fields.Many2one("project.milestone", "Milestone")

    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr,
                    t.id as id,
                    t.id as task_id,
                    t.create_date as create_date,
                    t.date_assign as date_assign,
                    t.date_end as date_end,
                    t.date_last_stage_update as date_last_stage_update,
                    t.date_deadline as date_deadline,
                    t.project_id,
                    t.milestone_id,
                    t.priority,
                    t.name as name,
                    t.company_id,
                    t.partner_id,
                    t.stage_id as stage_id,
                    t.kanban_state as state,
                    NULLIF(t.rating_last_value, 0) as rating_last_value,
                    t.working_days_close as working_days_close,
                    t.working_days_open  as working_days_open,
                    t.working_hours_open as working_hours_open,
                    t.working_hours_close as working_hours_close,
                    (extract('epoch' from (t.date_deadline-(now() at time zone 'UTC'))))/(3600*24)  as delay_endings_days
        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    t.id,
                    t.create_date,
                    t.write_date,
                    t.date_assign,
                    t.date_end,
                    t.date_deadline,
                    t.date_last_stage_update,

                    t.project_id,
                    t.priority,
                    t.milestone_id,
                    t.name,
                    t.company_id,
                    t.partner_id,
                    t.stage_id
        """
        return group_by_str
