# -*- coding: utf-8 -*-
"""Assessment"""


from odoo import fields, models, api, _
from datetime import datetime
from odoo import SUPERUSER_ID
from odoo.exceptions import ValidationError
from datetime import timedelta
import pytz


class Assessment(models.Model):
    """model for managing assessments"""
    _name = "assessment.assessment"
    _description = "Assessment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'partner_id'

    active = fields.Boolean('Active', default=True)
    datetime = fields.Datetime(string="Date-Time", required=True, Tracking=True,
                               default=lambda self: fields.Datetime.now())
    partner_id = fields.Many2one('res.partner', string="Member Name",
                                 required=True, Tracking=True)
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender", related='partner_id.gender')
    height = fields.Integer(string="Height (cm)", related='partner_id.height')
    age = fields.Integer(string="Age", related='partner_id.age')
    user_id = fields.Many2one('res.users', string="Coach", index=True,
                              tracking=True, default=lambda self: self.env.user)
    m_datetime = fields.Datetime(string="Date-Time", Tracking=True)
    weight = fields.Float(string="Weight (kg)", required=True)
    muscle_mass = fields.Float(string="Muscle Mass (kg)", required=True)
    fat_mass = fields.Float(string="Fat Mass (kg)", required=True)
    body_water = fields.Float(string="Body Water (kg)", required=True)
    w_h_ratio = fields.Float(string="Waist Hip Ratio", required=True)
    chest = fields.Float(string="Chest", required=True)
    arm = fields.Float(string="Arm", required=True)
    narrow_waist = fields.Float(string="Narrow Waist", required=True)
    waist = fields.Float(string="Waist", required=True)
    hips = fields.Float(string="Hips", required=True)
    glute_fold = fields.Float(string="Glute Fold", required=True)
    fat_free_mass = fields.Float(string="Fat Free Mass (kg)",
                                 compute='_compute_fat_free_mass', store=True)
    bmi = fields.Float(string="BMI", compute='_compute_bmi',
                       store=True)
    body_fat_perc = fields.Float(string="Body Fat %",
                                 compute='_compute_body_fat_perc', store=True)
    bmr = fields.Float(string="BMR", compute='_compute_bmr',
                       store=True)
    str_weight = fields.Text(string="Weight", compute='_compute_str_weight',
                             store=True)
    latest_record = fields.Boolean(string="Latest Record", store=True,
                                   copy=False)
    override_validation = fields.Boolean(string="Override Validation")
    o2o_datetime = fields.Datetime(string="Date-Time", Tracking=True)
    p_feedback = fields.Text(string="Positive Feedback")
    n_feedback = fields.Text(string="Negative Feedback")
    nutrition_plan = fields.Text(string="Nutrition Plan")
    training_plan = fields.Text(string="Training Plan")
    supplements = fields.Text(string="Supplements")
    medication = fields.Text(string="Medication")
    injuries = fields.Text(string="Injuries")
    menstrual_cycle = fields.Text(string="Menstrual Cycle")
    notes = fields.Text(string="Additional Notes")
    systolic_reading = fields.Integer(string="Systolic Reading")
    diastolic_reading = fields.Integer(string="Diastolic Reading")
    resting_heart_rate = fields.Integer(string="Resting Heart Reading")
    blood_sugar_level = fields.Integer(string="Blood Sugar Level")
    o2o_latest_record = fields.Boolean(string="Latest Record")
    img_date = fields.Date(string="Date")
    img_front = fields.Image(string="Front", max_width=500, max_height=1024,
                               copy=False)
    img_back = fields.Image(string="Back", max_width=500, max_height=1024,
                               copy=False)
    img_left = fields.Image(string="Left Side", max_width=500, max_height=1024,
                            copy=False)
    img_right = fields.Image(string="Right Side", max_width=500, max_height=1024,
                            copy=False)
    img_latest_record = fields.Boolean(string="Latest Record")

    # create
    @api.model
    def create(self, vals):
        """create methode"""
        result = super(Assessment, self).create(vals)
        return result

    # # compute methods
    # @api.depends('partner_id')
    # def _compute_latest_record(self):

    @api.depends('weight', 'fat_mass')
    def _compute_fat_free_mass(self):
        for assessment in self:
            assessment.fat_free_mass = assessment.weight - assessment.fat_mass

    @api.depends('partner_id', 'weight')
    def _compute_bmi(self):
        for assessment in self:
            assessment.bmi = 0
            sq_height = assessment.partner_id.height/100 * assessment.partner_id.height/100
            if sq_height > 0:
                bmi = assessment.weight/sq_height
                assessment.bmi = round(bmi, 1)

    @api.depends('fat_mass', 'weight')
    def _compute_body_fat_perc(self):
        for assessment in self:
            assessment.body_fat_perc = 0
            if assessment.weight > 0:
                perc = (assessment.fat_mass / assessment.weight) * 100
                assessment.body_fat_perc = round(perc, 1)

    @api.depends('fat_free_mass')
    def _compute_bmr(self):
        for assessment in self:
            bmr = 370 + (21.6 * assessment.fat_free_mass)
            assessment.bmr = round(bmr, 0)

    @api.depends('weight')
    def _compute_str_weight(self):
        for assessment in self:
            kgtost = assessment.weight / 6.35
            stones = int(kgtost)
            gtolb = assessment.weight / 6.35
            pounds = int((gtolb - stones) * 14)
            string = '%s ST %s lbs' % (stones, pounds)
            assessment.str_weight = string


class LogBenchmark(models.Model):
    """model for managing benchmark log"""
    _name = "log.benchmark"
    _description = "Benchmark"
    _rec_name = 'datetime'

    partner_id = fields.Many2one('res.partner', string="Member")
    datetime = fields.Datetime(string="Date-Time")
    old_value = fields.Float(string="Old Value")
    new_value = fields.Float(string="New Value")
