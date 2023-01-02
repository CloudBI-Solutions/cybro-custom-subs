from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import timedelta


class Partner(models.Model):
    _inherit = "res.partner"

    assessment_ids = fields.One2many(
        'assessment.assessment', 'partner_id', string="Assessments")
    latest_assessment_id = fields.Many2one(
        'assessment.assessment', string="Latest Assessment", store=True,
        copy=False, compute='_compute_latest_assessment_id')
    weight_goal = fields.Selection([
        ('fat_loss', 'Fat Loss'),
        ('maintain', 'Maintain'),
        ('muscle_gain', 'Muscle Gain')
    ], string="Weight Goal", tracking=True)
    benchmark_weight = fields.Float(string="Benchmark Weight (kg)", store=True)
    last_weight = fields.Float(string="Last Weight (kg)", store=True,
                               related='latest_assessment_id.weight')
    kg_weight_diff = fields.Float(
        string="Change in Weight (kg)", store=True, copy=False,
        compute='_compute_weight_differences')
    lbs_weight_diff = fields.Float(
        string="Change in Weight (lbs)", store=True, copy=False,
        compute='_compute_weight_differences')
    decorator_lbs_weight_diff = fields.Selection([
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('success', 'Success'),
    ], string="Decorator Weight Difference", store=True,
        compute='_compute_decorator_lbs_weight_diff')
    weight_30_days_ago = fields.Float(
        string="Weight 30 Days Ago (kg)", store=True, copy=False)
    kg_diff_rolling = fields.Float(
        string="Rolling Difference (kg)", store=True, copy=False,
        compute='_compute_rolling_differences')
    lbs_diff_rolling = fields.Float(
        string="Rolling Difference (lbs)", store=True, copy=False,
        compute='_compute_rolling_differences')
    decorator_lbs_diff_rolling = fields.Selection([
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('success', 'Success'),
    ], string="Decorator Rolling Difference", store=True,
        compute='_compute_decorator_lbs_diff_rolling')
    log_benchmark_ids = fields.One2many(
        'log.benchmark', 'partner_id', string="Benchmark Log")
    coach_id = fields.Many2one('res.users', string="Coach", copy=False)

    # write
    def write(self, vals):
        old_value = self.benchmark_weight
        res = super(Partner, self).write(vals)
        if 'benchmark_weight' in vals:
            log = self.env['log.benchmark'].create({
                'old_value': old_value,
                'new_value': self.benchmark_weight,
                'partner_id': self.id,
                'datetime': fields.Datetime.now()
            })
        return res

    @api.model
    def _compute_weight_30_days_ago(self):
        partners = self.env['res.partner'].search([])
        for partner in partners:
            partner_assessments = partner.assessment_ids
            obj_datetime = datetime.now() - timedelta(30)
            assessments = partner_assessments.search(
                [('datetime', '<=', obj_datetime),
                 ('partner_id', '=', partner.id)],
                order='datetime desc')
            print(assessments)
            assessment = partner_assessments.search(
                [('datetime', '<=', obj_datetime),
                 ('partner_id', '=', partner.id)],
                order='datetime desc', limit=1)
            if assessment:
                partner.weight_30_days_ago = assessment.weight

    @api.depends('assessment_ids')
    def _compute_latest_assessment_id(self):
        for contact in self:
            assessments = contact.assessment_ids
            assessments.latest_record = False
            latest_assessment = assessments.search(
                [('partner_id', '=', contact.id)],
                order='datetime desc', limit=1)
            contact.latest_assessment_id = latest_assessment.id
            latest_assessment.latest_record = True

    @api.depends('last_weight', 'weight_30_days_ago')
    def _compute_rolling_differences(self):
        for partner in self:
            kg_rolling_diff = partner.last_weight - partner.weight_30_days_ago
            partner.kg_diff_rolling = kg_rolling_diff
            partner.lbs_diff_rolling = kg_rolling_diff * 2.2

    @api.depends('last_weight', 'benchmark_weight')
    def _compute_weight_differences(self):
        for partner in self:
            kg_weight_diff = partner.last_weight - partner.benchmark_weight
            partner.kg_weight_diff = kg_weight_diff
            partner.lbs_weight_diff = kg_weight_diff * 2.2
            if partner.lbs_weight_diff >= 7:
                partner.benchmark_weight = partner.last_weight

    @api.depends('weight_goal', 'lbs_weight_diff')
    def _compute_decorator_lbs_weight_diff(self):
        for partner in self:
            if partner.weight_goal == 'fat_loss':
                if partner.lbs_weight_diff < 0:
                    partner.decorator_lbs_weight_diff = "success"
                elif partner.lbs_weight_diff > 0:
                    partner.decorator_lbs_weight_diff = "danger"
                else:
                    partner.decorator_lbs_weight_diff = "warning"
            elif partner.weight_goal == 'maintain':
                if partner.lbs_weight_diff == 0:
                    partner.decorator_lbs_weight_diff = "success"
                elif -0.5 <= partner.lbs_weight_diff >= 0.5:
                    partner.decorator_lbs_weight_diff = "warning"
                else:
                    partner.decorator_lbs_weight_diff = "danger"
            elif partner.weight_goal == 'muscle_gain':
                if partner.lbs_weight_diff > 0:
                    partner.decorator_lbs_weight_diff = "success"
                elif partner.lbs_weight_diff < 0:
                    partner.decorator_lbs_weight_diff = "danger"
                else:
                    partner.decorator_lbs_weight_diff = "warning"
            else:
                partner.decorator_lbs_weight_diff = False

    @api.depends('weight_goal', 'lbs_diff_rolling')
    def _compute_decorator_lbs_diff_rolling(self):
        for partner in self:
            if partner.weight_goal == 'fat_loss':
                if partner.lbs_diff_rolling < 0:
                    partner.decorator_lbs_diff_rolling = "success"
                elif partner.lbs_diff_rolling > 0:
                    partner.decorator_lbs_diff_rolling = "danger"
                else:
                    partner.decorator_lbs_diff_rolling = "warning"
            elif partner.weight_goal == 'maintain':
                if partner.lbs_diff_rolling == 0:
                    partner.decorator_lbs_diff_rolling = "success"
                elif -0.5 <= partner.lbs_diff_rolling >= 0.5:
                    partner.decorator_lbs_diff_rolling = "warning"
                else:
                    partner.decorator_lbs_diff_rolling = "danger"
            elif partner.weight_goal == 'muscle_gain':
                if partner.lbs_diff_rolling > 0:
                    partner.decorator_lbs_diff_rolling = "success"
                elif partner.lbs_diff_rolling < 0:
                    partner.decorator_lbs_diff_rolling = "danger"
                else:
                    partner.decorator_lbs_diff_rolling = "warning"
            else:
                partner.decorator_lbs_diff_rolling = False
