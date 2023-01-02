# -*- coding: utf-8 -*-
"""assessments"""

from odoo.addons.http_routing.models.ir_http import slug
from odoo import fields, models, api, _
from random import randint
from dateutil.relativedelta import relativedelta
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError
import json
import itertools


class Assessments(models.Model):
    """model for managing assessments"""
    _name = "assessment.assessment"
    _description = "Assessments"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Name", readonly=True, )
    stage_id = fields.Many2one(
        'assessment.stage', string='Stage', index=True, tracking=True,
        readonly=False, store=True, copy=False, ondelete='restrict',
        default=lambda self: self._default_stage_id(),
        group_expand='_read_group_stage_ids')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    partner_id = fields.Many2one('paceflow.client', string="Coach",
                                 required=True,
                                 store=True, tracking=True)
    child_id = fields.Many2one("paceflow.child", 'Player', required=True,
                               store=True, tracking=True)
    phone = fields.Char('Phone', related='partner_id.phone', readonly=False)
    email = fields.Char('Email', related='partner_id.email', readonly=False)
    sale_order_id = fields.Many2one('sale.order', string="Sales Order")
    report_date = fields.Date(string="Report Date")
    done_date = fields.Date(string="Date Done")
    tag_ids = fields.Many2many('assessment.tags', string='Tags')
    coach_id = fields.Many2one('res.users', string="Responsible", tracking=True)
    hand = fields.Selection([('left', 'Left Handed'), ('right', 'Right Handed')
                             ], string="Hand")
    dob = fields.Date(string="DOB", )
    age = fields.Integer(string="Age", compute='_compute_age')
    ball_size = fields.Selection([('junior', 'Junior'), ('men', 'Men'),
                                  ('women', 'Women')], string="Ball Size")
    highest_standard = fields.Selection(
        [('professional', 'Professional'),
         ('country_academy', 'Country Academy'),
         ('country_age_group', 'Country Age Group'),
         ('club_cricket', 'Club Cricket'),
         ('non_competitive', 'Non-Competitive')],
        string="Highest Standard Played")
    velocity = fields.Float(string="Ball Velocity")
    attachment_ids = fields.Many2many(
        'ir.attachment', 'assessment_ir_attachments_rel',
        'assessment_id', 'attachment_id', string='Attachments')
    # summary_fields
    legality = fields.Selection([('failed', 'Failed'), ('passed', 'Passed')
                                 ], string="Legality")
    summary_overall_score = fields.Float(
        string="Overall Score",
        compute="_compute_summary_overall_score")
    summary_side_view = fields.Image('Side view', copy=False, attachment=True,
                                     max_width=1024, max_height=1024)
    summary_rear_view = fields.Image('Rear view', copy=False, attachment=True,
                                     max_width=1024, max_height=1024)
    drill_ids = fields.Many2many('slide.slide', compute='_compute_drill_ids',
                                 store=True, readonly=True,
                                 string="Drills")
    summary_note_ids = fields.Many2many(
        'comment.comment', compute='_compute_summary_note_ids', store=True,
        readonly=True, string="Summary Comments")
    # legality_fields
    new_integer = fields.Float(string="Overall legality score",
                               compute="_compute_new_integer")
    legality_score = fields.Integer(string="Legality", default=0)
    phase_1_selection = fields.Integer(string="Phase 1", default=0)
    phase_2_selection = fields.Integer(string="Phase 2", default=0)
    phase_3_selection = fields.Integer(string="Phase 3", default=0)
    phase_4_selection = fields.Integer(string="Phase 4", default=0)
    img_phase_1 = fields.Image(string="Phase 1", max_width=500, max_height=1024,
                               copy=False)
    img_phase_2 = fields.Image(string="Phase 2", max_width=500, max_height=1024,
                               copy=False)
    img_phase_3 = fields.Image(string="Phase 3", max_width=500, max_height=1024,
                               copy=False)
    img_phase_4 = fields.Image(string="Phase 4", max_width=500, max_height=1024,
                               copy=False)
    legality_video = fields.Binary(string="Legality Video")
    legality_drill_ids = fields.Many2many(
        'slide.slide', 'slide_legality_rel', 'drill_id', 'assessment_id',
        string="Legality drills", store=True,
        domain="[('is_drill', '=', True), ('legality', '=', True)]")
    legality_note_ids = fields.Many2many(
        'comment.comment', 'comment_legality_rel', 'comment_id',
        'assessment_id', string="Legality Comments", store=True,
        domain="[('legality', '=', True)]")
    # momentum fields
    momentum_score = fields.Float(string="Overall momentum score",
                                  compute="_compute_momentum_score")
    momentum_speed = fields.Float(string="Momentum Speed (m/s)")
    cadence_efficiency_selection = fields.Integer(
        string="Cadence/Efficiency", default=0)
    cadence_tempo_selection = fields.Integer(
        string="Cadence/Tempo", default=0)
    cadence_stride_selection = fields.Integer(
        string="Cadence/Stride length(% Difference)", default=0)
    img_cadence_efficiency = fields.Image(
        'Cadence/Efficiency', attachment=True, max_width=500, max_height=1024,
        copy=False)
    img_cadence_tempo = fields.Image(
        'Cadence/Tempo', attachment=True, max_width=500, max_height=1024,
        copy=False)
    img_cadence_stride = fields.Image(
        'Cadence/Stride length(% Difference)', attachment=True, max_width=500,
        max_height=1024, copy=False)
    momentum_drill_ids = fields.Many2many(
        'slide.slide', 'slide_momentum_rel', 'drill_id', 'assessment_id',
        string="Momentum drills", store=True,
        domain="[('is_drill', '=', True), ('momentum', '=', True)]")
    momentum_note_ids = fields.Many2many(
        'comment.comment', 'comment_momentum_rel', 'comment_id',
        'assessment_id', string="Momentum Comments", store=True,
        domain="[('momentum', '=', True)]")
    # stability fields
    stability_score = fields.Float(string="Overall stability score",
                                   compute="_compute_stability_score")
    lp_selection = fields.Integer(
        string="Bowling arm slot LP", default=0)
    hp_selection = fields.Integer(
        string="Bowling arm slot HP", default=0)
    lhcd_selection = fields.Integer(
        string="Lower half change of direction", default=0)
    cm_bfc_selection = fields.Integer(
        string="CM direction to BFC", default=0)
    bfc_selection = fields.Integer(
        string="Front leg angle BFC", default=0)
    bla_bfc_selection = fields.Integer(
        string="Back leg angles BFC", default=0)
    rb_bfc_selection = fields.Integer(
        string="Rock back BFC", default=0)
    h_bfc_selection = fields.Integer(
        string="Hinge BFC", default=0)
    bad_bfc_selection = fields.Integer(
        string="Bowling arm delay at BFC", default=0)
    cm_bfc_ffc_selection = fields.Integer(
        string="CM direction BFC to FFC", default=0)
    fa_bfc_selection = fields.Integer(
        string="Front arm at BFC", default=0)
    img_lp = fields.Image('LP', attachment=True,
                          max_width=500, max_height=1024, copy=False)
    img_fp = fields.Image('HP', attachment=True,
                          max_width=500, max_height=1024, copy=False)
    img_lhcd = fields.Image('LHCD', attachment=True,
                            max_width=500, max_height=1024, copy=False)
    img_cm_bfc = fields.Image('CM-BFC', attachment=True,
                              max_width=500, max_height=1024, copy=False)
    img_bfc = fields.Image('BFC', attachment=True,
                           max_width=500, max_height=1024, copy=False)
    img_bfc_side = fields.Image('BFC Side view', attachment=True,
                                max_width=500, max_height=1024, copy=False)
    img_bfc_rear = fields.Image('BFC Rear view', attachment=True,
                                max_width=500, max_height=1024, copy=False)
    img_rb_bfc = fields.Image('BFC Side view', attachment=True,
                              max_width=500, max_height=1024, copy=False)
    img_h_bfc = fields.Image('BFC Side view', attachment=True,
                             max_width=500, max_height=1024, copy=False)
    img_bad_bfc = fields.Image('BFC Side view', attachment=True,
                               max_width=500, max_height=1024, copy=False)
    img_cm_bfc_ffc = fields.Image('BFC Side view', attachment=True,
                                  max_width=500, max_height=1024, copy=False)
    img_fa_bfc = fields.Image('BFC Side view', attachment=True,
                              max_width=500, max_height=1024, copy=False)
    stability_drill_ids = fields.Many2many(
        'slide.slide', 'slide_stability_rel', 'drill_id', 'assessment_id',
        string="Stability drills", store=True,
        domain="[('is_drill', '=', True), ('stability', '=', True)]")
    stability_note_ids = fields.Many2many(
        'comment.comment', 'comment_stability_rel', 'comment_id',
        'assessment_id', string="Stability Comments", store=True,
        domain="[('stability', '=', True)]")
    # paceflow fields
    paceflow_score = fields.Float(string="Overall pace-flow score",
                                  compute="_compute_paceflow_score")
    heel_strike_selection = fields.Integer(
        string="Heel strike", default=0)
    front_arm_position_selection = fields.Integer(
        string="Front arm position", default=0)
    delayed_bowling_arm_selection = fields.Integer(
        string="Delayed bowling arm", default=0)
    pelvis_control_selection = fields.Integer(
        string="Pelvis Control", default=0)
    side_flexion_selection = fields.Integer(
        string="Side Flexion", default=0)
    front_knee_selection = fields.Integer(
        string="Front Knee", default=0)
    top_half_selection = fields.Integer(
        string="Top Half", default=0)
    front_arm_end_point_selection = fields.Integer(
        string="Front arm end point", default=0)
    shoulder_delay_selection = fields.Integer(
        string="Shoulder delay", default=0)
    ft_energy_selection = fields.Integer(
        string="Follow through energy", default=0)
    ft_direction_selection = fields.Integer(
        string="Follow through direction", default=0)
    img_heel_strike = fields.Image('FFC side view', store=True,
                                   max_width=500, max_height=1024, copy=False)
    img_front_arm_position = fields.Image('FFC side view', store=True,
                                  max_width=500, max_height=1024, copy=False)
    img_delayed_bowling_arm = fields.Image('FFC side view', store=True,
                                   max_width=500, max_height=1024, copy=False)
    img_pelvis_control = fields.Image('FFC rear view', store=True,
                              max_width=500, max_height=1024, copy=False)
    img_side_flexion = fields.Image('Ball release rear view', store=True,
                                    max_width=500, max_height=1024, copy=False)
    img_front_knee = fields.Image('Ball release side view', store=True,
                                  max_width=500, max_height=1024, copy=False)
    img_top_half_1 = fields.Image('Ball release side view', store=True,
                                  max_width=500, max_height=1024, copy=False)
    img_top_half_2 = fields.Image('FFC Side view', store=True,
                                  max_width=500, max_height=1024, copy=False)
    img_front_arm_end_point = fields.Image('Ball release rear view', store=True,
                                           max_width=500, max_height=1024,
                                           copy=False)
    img_shoulder_delay = fields.Image('Ball release side view', store=True,
                                      max_width=500, max_height=1024,
                                      copy=False)
    img_ft_energy = fields.Image('Follow through step side view', store=True,
                                 max_width=500, max_height=1024,
                                 copy=False)
    img_ft_direction = fields.Image('Follow through 1,2,3 rear view',
                                    store=True,
                                    max_width=500, max_height=1024,
                                    copy=False)
    paceflow_drill_ids = fields.Many2many(
        'slide.slide', 'slide_paceflow_rel', 'drill_id', 'assessment_id',
        string="Paceflow drills", store=True,
        domain="[('is_drill', '=', True), ('paceflow', '=', True)]")
    paceflow_note_ids = fields.Many2many(
        'comment.comment', 'comment_paceflow_rel', 'comment_id',
        'assessment_id', string="Paceflow Comments", store=True,
        domain="[('paceflow', '=', True)]")
    rear_video = fields.Binary(copy=False)
    rear_reference = fields.Char(copy=False)
    side_video = fields.Binary(copy=False)
    side_reference = fields.Char(copy=False)
    img_stability_overall_1 = fields.Image(string="Stability Overall 1",
                                           max_width=500, max_height=1024,
                                           copy=False, store=True)
    img_stability_overall_2 = fields.Image(string="Stability Overall 2",
                                           max_width=500, max_height=1024,
                                           copy=False, store=True)
    img_legality_overall = fields.Image(string="Legality Overall", store=True,
                                        max_width=500, max_height=1024,
                                        copy=False)
    img_momentum_overall = fields.Image(string="Momentum Overall", store=True,
                                        max_width=500, max_height=1024,
                                        copy=False)
    img_summary_overall_1 = fields.Image(string="Summary Overall 1",
                                         max_width=500, max_height=1024,
                                         copy=False, store=True)
    img_summary_overall_2 = fields.Image(string="Summary Overall 2",
                                         max_width=500, max_height=1024,
                                         copy=False, store=True)
    img_paceflow_overall_1 = fields.Image(string="Paceflow Overall 1",
                                          max_width=500, max_height=1024,
                                          copy=False, store=True)
    img_paceflow_overall_2 = fields.Image(string="Paceflow Overall 2",
                                          max_width=500, max_height=1024,
                                          copy=False, store=True)
    section_legality_id = fields.Many2one('slide.slide', readonly=True)
    section_momentum_id = fields.Many2one('slide.slide', readonly=True)
    section_stability_id = fields.Many2one('slide.slide', readonly=True)
    section_paceflow_id = fields.Many2one('slide.slide', readonly=True)
    section_legality_note_id = fields.Many2one('comment.comment', readonly=True)
    section_momentum_note_id = fields.Many2one('comment.comment', readonly=True)
    section_stability_note_id = fields.Many2one('comment.comment',
                                                readonly=True)
    section_paceflow_note_id = fields.Many2one('comment.comment', readonly=True)

    # create
    @api.model
    def create(self, vals):
        """create methode"""
        result = super(Assessments, self).create(vals)
        section_legality = self.env["slide.slide"].create({
            'name': 'Legality Drills',
            'channel_id': 1,
            'is_category': True,
        })
        section_legality_note = self.env["comment.comment"].create({
            'name': 'Legality Notes',
            'description': "Section",
            'is_category': True,
        })
        result.section_legality_id = section_legality.id
        result.section_legality_note_id = section_legality_note.id
        section_momentum = self.env["slide.slide"].create({
            'name': 'Momentum Drills',
            'channel_id': 1,
            'is_category': True,
        })
        section_momentum_note = self.env["comment.comment"].create({
            'name': 'Momentum Notes',
            'description': "Section",
            'is_category': True,
        })
        result.section_momentum_id = section_momentum.id
        result.section_momentum_note_id = section_momentum_note.id
        section_stability = self.env["slide.slide"].create({
            'is_category': True,
            'name': 'Stability Drills',
            'channel_id': 1
        })
        section_stability_note = self.env["comment.comment"].create({
            'is_category': True,
            'name': 'Stability Notes',
            'description': "Section",
        })
        result.section_stability_note_id = section_stability_note.id
        result.section_stability_id = section_stability.id
        section_paceflow = self.env["slide.slide"].create({
            'is_category': True,
            'name': 'Paceflow Drills',
            'channel_id': 1
        })
        section_paceflow_note = self.env["comment.comment"].create({
            'is_category': True,
            'name': 'Paceflow Notes',
            'description': "Section",
        })
        result.section_paceflow_note_id = section_paceflow_note.id
        result.section_paceflow_id = section_paceflow.id
        return result

    def set_record_img(self, *args):
        # setting image for record
        record = self
        img = args[0].get('image')
        striped_img = img.replace('data:image/png;base64,', '')
        if args[0].get('button_name') == 'Phase1':
            record.write({'img_phase_1': striped_img})
        elif args[0].get('button_name') == 'Phase2':
            record.write({'img_phase_2': striped_img})
        elif args[0].get('button_name') == 'Phase3':
            record.write({'img_phase_3': striped_img})
        elif args[0].get('button_name') == 'Phase4':
            record.write({'img_phase_4': striped_img})
        elif args[0].get('button_name') == 'Cadence/Efficiency':
            record.write({'img_cadence_efficiency': striped_img})
        elif args[0].get('button_name') == 'Cadence/Tempo':
            record.write({'img_cadence_tempo': striped_img})
        elif args[0].get('button_name') == 'Cadence/Stridelength':
            record.write({'img_cadence_stride': striped_img})
        elif args[0].get('button_name') == 'LP':
            record.write({'img_lp': striped_img})
        elif args[0].get('button_name') == 'HP':
            record.write({'img_fp': striped_img})
        elif args[0].get('button_name') == 'LHCD':
            record.write({'img_lhcd': striped_img})
        elif args[0].get('button_name') == 'CM-BFC':
            record.write({'img_cm_bfc': striped_img})
        elif args[0].get('button_name') == 'BFC':
            record.write({'img_bfc': striped_img})
        elif args[0].get('button_name') == 'BFCSideview':
            record.write({'img_bfc_side': striped_img})
        elif args[0].get('button_name') == 'BlaBFCRearview':
            record.write({'img_bfc_rear': striped_img})
        elif args[0].get('button_name') == 'BlaBFCSideview':
            record.write({'img_rb_bfc': striped_img})
        elif args[0].get('button_name') == 'HBFCSideview':
            record.write({'img_h_bfc': striped_img})
        elif args[0].get('button_name') == 'BadaBFC':
            record.write({'img_bad_bfc': striped_img})
        elif args[0].get('button_name') == 'CMdBFCtFFC':
            record.write({'img_cm_bfc_ffc': striped_img})
        elif args[0].get('button_name') == 'FaaBFC':
            record.write({'img_fa_bfc': striped_img})
        elif args[0].get('button_name') == 'Hs':
            record.write({'img_heel_strike': striped_img})
        elif args[0].get('button_name') == 'Fap':
            record.write({'img_front_arm_position': striped_img})
        elif args[0].get('button_name') == 'Dba':
            record.write({'img_delayed_bowling_arm': striped_img})
        elif args[0].get('button_name') == 'PC':
            record.write({'img_pelvis_control': striped_img})
        elif args[0].get('button_name') == 'SF':
            record.write({'img_side_flexion': striped_img})
        elif args[0].get('button_name') == 'FK':
            record.write({'img_front_knee': striped_img})
        elif args[0].get('button_name') == 'THBrsv':
            record.write({'img_top_half_1': striped_img})
        elif args[0].get('button_name') == 'THFFCsv':
            record.write({'img_top_half_2': striped_img})
        elif args[0].get('button_name') == 'Faep':
            record.write({'img_front_arm_end_point': striped_img})
        elif args[0].get('button_name') == 'Sd':
            record.write({'img_shoulder_delay': striped_img})
        elif args[0].get('button_name') == 'Fte':
            record.write({'img_ft_energy': striped_img})
        elif args[0].get('button_name') == 'Ftd':
            record.write({'img_ft_direction': striped_img})

    def get_current_record(self):
        # This function is used to get record in js
        items_lits = []
        print("hereee")
        for rec in self.attachment_ids:
            items_lits.append({'data': rec.datas,
                               'upd_date': rec.upload_date,
                               'reference': rec.reference})
        return items_lits

    def _default_stage_id(self):
        """Setting default stage"""
        rec = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_assessment').id)
        return rec.id if rec else None

    @api.model
    def _read_group_stage_ids(self, categories, domain, order):
        """ Read all the stages and display it in the kanban view,
            even if it is empty."""
        category_ids = categories._search([], order=order,
                                          access_rights_uid=SUPERUSER_ID)
        return categories.browse(category_ids)

    # dashboard data fetching methods

    @api.model
    def get_history_dashboard_data(self, assessment_id):
        assessment = self.env['assessment.assessment'].browse(assessment_id)
        y_axis = []
        x_axis = ['Velocity', 'Legality', 'Momentum', 'Stability', 'Paceflow']
        y_axis.append(assessment.velocity)
        y_axis.append(assessment.new_integer)
        y_axis.append(assessment.momentum_score)
        y_axis.append(assessment.stability_score)
        y_axis.append(assessment.paceflow_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @api.model
    def get_speed_dashboard_data(self, child_id):
        # Optimization
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_done').id)

        assessments = self.env['assessment.assessment'].search(
            [('stage_id', '=', stage.id), ('child_id', '=', int(child_id))],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.velocity)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @api.model
    def get_score_dashboard_data(self, child_id):
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_done').id)

        assessments = self.env['assessment.assessment'].search(
            [('stage_id', '=', stage.id), ('child_id', '=', int(child_id))],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.summary_overall_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @api.model
    def get_legality_dashboard_data(self, child_id):
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_done').id)

        assessments = self.env['assessment.assessment'].search(
            [('stage_id', '=', stage.id), ('child_id', '=', int(child_id))],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.new_integer)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @api.model
    def get_runup_dashboard_data(self, child_id):
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_done').id)

        assessments = self.env['assessment.assessment'].search(
            [('stage_id', '=', stage.id), ('child_id', '=', int(child_id))],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.momentum_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @api.model
    def get_stride_dashboard_data(self, child_id):
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_done').id)

        assessments = self.env['assessment.assessment'].search(
            [('stage_id', '=', stage.id), ('child_id', '=', int(child_id))],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.stability_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @api.model
    def get_ffc_dashboard_data(self, child_id):
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_done').id)

        assessments = self.env['assessment.assessment'].search(
            [('stage_id', '=', stage.id), ('child_id', '=', int(child_id))],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.paceflow_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    @api.model
    def get_ft_dashboard_data(self, child_id):
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_done').id)

        assessments = self.env['assessment.assessment'].search(
            [('stage_id', '=', stage.id), ('child_id', '=', int(child_id))],
            order='done_date asc', limit=10)
        x_axis = []
        y_axis = []
        for assessment in assessments:
            x_axis.append(assessment.name)
            y_axis.append(assessment.br_ft_score)
        data = {
            'x_axis': x_axis,
            'y_axis': y_axis
        }
        return data

    # compute methods

    @api.depends('legality_drill_ids', 'momentum_drill_ids',
                 'stability_drill_ids', 'paceflow_drill_ids')
    def _compute_drill_ids(self):
        for assessment in self:
            drill_ids = []
            sequence = 1
            legality_drills = self.env['slide.slide'].browse(
                assessment.legality_drill_ids.ids)
            momentum_drills = self.env['slide.slide'].browse(
                assessment.momentum_drill_ids.ids)
            stability_drills = self.env['slide.slide'].browse(
                assessment.stability_drill_ids.ids)
            paceflow_drills = self.env['slide.slide'].browse(
                assessment.paceflow_drill_ids.ids)
            if assessment.section_legality_id:
                drill_ids.append(assessment.section_legality_id.id)
                assessment.section_legality_id.order_sequence = sequence
                sequence += 1
            for legality_drill in legality_drills:
                legality_drill.order_sequence = sequence
                drill_ids.append(legality_drill.id)
                sequence += 1
            if assessment.section_momentum_id:
                drill_ids.append(assessment.section_momentum_id.id)
                assessment.section_momentum_id.order_sequence = sequence
                sequence += 1
            for momentum_drill in momentum_drills:
                momentum_drill.order_sequence = sequence
                drill_ids.append(momentum_drill.id)
                sequence += 1
            if assessment.section_stability_id:
                drill_ids.append(assessment.section_stability_id.id)
                assessment.section_stability_id.order_sequence = sequence
                sequence += 1
            for stability_drill in stability_drills:
                stability_drill.order_sequence = sequence
                drill_ids.append(stability_drill.id)
                sequence += 1
            if assessment.section_paceflow_id:
                drill_ids.append(assessment.section_paceflow_id.id)
                assessment.section_paceflow_id.order_sequence = sequence
                sequence += 1
            for paceflow_drill in paceflow_drills:
                paceflow_drill.order_sequence = sequence
                drill_ids.append(paceflow_drill.id)
                sequence += 1
            assessment.drill_ids = drill_ids

    @api.depends('legality_note_ids', 'momentum_note_ids',
                 'stability_note_ids', 'paceflow_note_ids')
    def _compute_summary_note_ids(self):
        for assessment in self:
            note_ids = []
            sequence = 1
            legality_notes = self.env['comment.comment'].browse(
                assessment.legality_note_ids.ids)
            momentum_notes = self.env['comment.comment'].browse(
                assessment.momentum_note_ids.ids)
            stability_notes = self.env['comment.comment'].browse(
                assessment.stability_note_ids.ids)
            paceflow_notes = self.env['comment.comment'].browse(
                assessment.paceflow_note_ids.ids)
            if assessment.section_legality_note_id:
                note_ids.append(assessment.section_legality_note_id.id)
                assessment.section_legality_note_id.order_sequence = sequence
                sequence += 1
            for legality_note in legality_notes:
                note_ids.append(legality_note.id)
                legality_note.order_sequence = sequence
                sequence += 1
            if assessment.section_momentum_note_id:
                note_ids.append(assessment.section_momentum_note_id.id)
                assessment.section_momentum_note_id.order_sequence = sequence
                sequence += 1
            for momentum_note in momentum_notes:
                note_ids.append(momentum_note.id)
                momentum_note.order_sequence = sequence
                sequence += 1
            if assessment.section_stability_note_id:
                note_ids.append(assessment.section_stability_note_id.id)
                assessment.section_stability_note_id.order_sequence = sequence
                sequence += 1
            for stability_note in stability_notes:
                note_ids.append(stability_note.id)
                stability_note.order_sequence = sequence
                sequence += 1
            if assessment.section_paceflow_note_id:
                note_ids.append(assessment.section_paceflow_note_id.id)
                assessment.section_paceflow_note_id.order_sequence = sequence
                sequence += 1
            for paceflow_note in paceflow_notes:
                note_ids.append(paceflow_note.id)
                paceflow_note.order_sequence = sequence
                sequence += 1
            assessment.summary_note_ids = note_ids

    @api.depends('dob')
    def _compute_age(self):
        # Get the current date
        today = fields.Date.today()
        for rec in self:
            rec.age = 0
            if rec.dob:
                # Get the difference between the current date and the birthday
                age = relativedelta(today, rec.dob)
                rec.age = age.years

    @api.depends('new_integer', 'momentum_score', 'stability_score',
                 'paceflow_score')
    def _compute_summary_overall_score(self):
        for assessment in self:
            score_all = assessment.new_integer + assessment.momentum_score + \
                        assessment.stability_score + assessment.paceflow_score
            assessment.summary_overall_score = score_all / 4

    @api.depends('phase_1_selection', 'phase_2_selection', 'phase_3_selection',
                 'phase_4_selection')
    def _compute_new_integer(self):
        for assessment in self:
            score_all = assessment.phase_1_selection + assessment.phase_2_selection + \
                        assessment.phase_3_selection + assessment.phase_4_selection
            assessment.new_integer = score_all / 4

    @api.depends('cadence_efficiency_selection', 'cadence_tempo_selection',
                 'cadence_stride_selection')
    def _compute_momentum_score(self):
        for assessment in self:
            assessment.momentum_score = (assessment.cadence_efficiency_selection
                                         + assessment.cadence_tempo_selection +
                                         assessment.cadence_stride_selection) / 3

    @api.depends('lp_selection', 'hp_selection', 'lhcd_selection',
                 'cm_bfc_selection', 'bfc_selection', 'bla_bfc_selection',
                 'rb_bfc_selection', 'h_bfc_selection', 'bad_bfc_selection',
                 'cm_bfc_ffc_selection', 'fa_bfc_selection')
    def _compute_stability_score(self):
        for assessment in self:
            score_all = assessment.lp_selection + assessment.hp_selection + assessment.lhcd_selection + assessment.cm_bfc_selection + \
                        assessment.bfc_selection + assessment.bla_bfc_selection + assessment.rb_bfc_selection + assessment.h_bfc_selection + \
                        assessment.bad_bfc_selection + assessment.cm_bfc_ffc_selection + assessment.fa_bfc_selection
            assessment.stability_score = score_all / 11

    @api.depends('heel_strike_selection', 'front_arm_position_selection',
                 'delayed_bowling_arm_selection', 'pelvis_control_selection',
                 'side_flexion_selection', 'front_knee_selection',
                 'top_half_selection', 'front_arm_end_point_selection',
                 'shoulder_delay_selection', 'ft_energy_selection',
                 'ft_direction_selection')
    def _compute_paceflow_score(self):
        for assessment in self:
            score_all = assessment.heel_strike_selection + assessment.front_arm_position_selection + \
                        assessment.delayed_bowling_arm_selection + assessment.pelvis_control_selection + \
                        assessment.side_flexion_selection + assessment.front_knee_selection + assessment.top_half_selection + \
                        assessment.front_arm_end_point_selection + assessment.shoulder_delay_selection + \
                        assessment.ft_energy_selection + assessment.ft_direction_selection
            assessment.paceflow_score = score_all / 11

    # button actions

    def assign_and_send_mail(self):
        if not self.coach_id:
            raise UserError(
                _('Please assign a Responsible before sending mail'))
        template_id = self.env.ref('paceflow.assign_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_assigned').id)
        self.write({'stage_id': stage.id})

    def make_in_progress(self):
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_in_progress').id)
        self.write({'stage_id': stage.id})

    def assessment_done(self):
        template_id = self.env.ref('paceflow.done_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_done').id)
        self.write({'stage_id': stage.id, 'done_date': fields.Date.today()})

    def cancel_assessment(self):
        stage = self.env['assessment.stage'].browse(
            self.env.ref('paceflow.stage_cancel').id)
        self.write({'stage_id': stage.id})


class AssessmentTags(models.Model):
    """ Tags of assessments """
    _name = "assessment.tags"
    _description = "Assessment Tags"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Name', required=True)
    color = fields.Integer(string='Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]


class AssessmentStages(models.Model):
    """ Stages of assessments """
    _name = "assessment.stage"
    _description = "Assessment Stages"
    _order = "sequence, id"
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
