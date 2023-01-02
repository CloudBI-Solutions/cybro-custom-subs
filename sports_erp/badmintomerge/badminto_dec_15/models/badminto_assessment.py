from odoo import models, fields, api
from random import randint
from odoo import SUPERUSER_ID


class BadmintoAssessment(models.Model):
    _name = 'badminto.assessment'
    _description = "Badminto Assessments"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Name', readonly=True)

    stage_id = fields.Many2one(
        'badminto.assessment.stage', string='Stage', index=True, tracking=True,
        readonly=False, store=True, copy=False, ondelete='restrict',
        default=lambda self: self._default_stage_id(),
        group_expand='_read_group_stage_ids')

    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    partner_id = fields.Many2one('organisation.coaches', string='Coach',
                                 required=True, store=True, tracking=True)
    athlete_id = fields.Many2one("organisation.athletes", 'Athlete',
                                 required=True, store=True, tracking=True)
    phone = fields.Char('Phone', related='partner_id.phone', readonly=False)
    email = fields.Char('Email', related='partner_id.email', readonly=False)
    report_date = fields.Date(string="Report Date")
    done_date = fields.Date(string="Date Done")

    tag_ids = fields.Many2many('badminto.assessment.tags', string='Tags')

    coach_id = fields.Many2one(
        'res.users',
        string="Responsible",
        tracking=True,
        domain=[('org_group_selection', '=', 'ex_coaches')])

    organisation_id = fields.Many2one('organisation.organisation',
                                      string='Organisation')

    hand = fields.Selection([('left', 'Left Handed'),
                             ('right', 'Right Handed')])

    highest_standard = fields.Selection(
        [('club', 'Club '),
         ('country', 'Country'),
         ('national', 'National'),
         ('international', 'International'),
         ('elite', 'Elite'),
         ('world_top', 'World Top'),
         ],
        string="Highest Standard Played", )

    dob = fields.Date(string="DOB", related='athlete_id.dob')
    age = fields.Integer(string="Age", related='athlete_id.age')
    active = fields.Boolean('Active', default=True)

    attachment_ids = fields.Many2many(
        'ir.attachment', 'badminto_ir_attachments_rel',
        'badminto_assessment_id', 'attachment_id', string='Attachments')

    s_r = fields.Boolean(string='Service/ Receiving Assessment')
    fnz = fields.Boolean(string='FNZ Assessment')
    bnz = fields.Boolean(string='BNZ Assessment')
    fmz = fields.Boolean(string='FMZ Assessment')
    bmz = fields.Boolean(string='BMZ Assessment')
    rcovhz = fields.Boolean(string='RCOvhZ Assessment')
    rcbz = fields.Boolean(string='RCBZ Assessment')
    rcfz = fields.Boolean(string='RCFZ Assessment')
    footwork = fields.Boolean(string='Footwork Patterns')

    # SR SERVICE
    overall_in_service = fields.Float(string='Overall',
                                      compute="get_overall_in_service")

    service_grip = fields.Integer(
        string="Grip", default=0)
    service_sp = fields.Integer(
        string="Starting Position", default=0)
    service_bp = fields.Integer(
        string="Backswing Position", default=0)
    service_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    service_fs = fields.Integer(
        string="Forward Swing", default=0)
    service_toi = fields.Integer(
        string="Time of Impact", default=0)
    service_ft = fields.Integer(
        string="Follow Through", default=0)

    service_video = fields.Binary('Service Video', attachment=True,
                                  copy=False)

    @api.depends('service_grip', 'service_sp', 'service_bp',
                 'service_be', 'service_fs', 'service_toi',
                 'service_ft')
    def get_overall_in_service(self):
        for rec in self:
            rec.overall_in_service = (rec.service_grip + rec.service_sp +
                                      rec.service_bp + rec.service_be +
                                      rec.service_fs + rec.service_toi +
                                      rec.service_ft) / 7

    # SR RECEIVING

    overall_in_receiving = fields.Float(string='Overall',
                                        compute="get_overall_in_receiving")

    receiving_grip = fields.Integer(
        string="Grip", default=0)
    receiving_sp = fields.Integer(
        string="Starting Position", default=0)
    receiving_bp = fields.Integer(
        string="Backswing Position", default=0)
    receiving_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    receiving_fs = fields.Integer(
        string="Forward Swing", default=0)
    receiving_toi = fields.Integer(
        string="Time of Impact", default=0)
    receiving_ft = fields.Integer(
        string="Follow Through", default=0)

    receiving_video = fields.Binary('Receiving Video', attachment=True,
                                    copy=False)

    @api.depends('receiving_grip', 'receiving_sp', 'receiving_bp',
                 'receiving_be', 'receiving_fs', 'receiving_toi',
                 'receiving_ft')
    def get_overall_in_receiving(self):
        for rec in self:
            rec.overall_in_receiving = (rec.receiving_grip + rec.receiving_sp +
                                        rec.receiving_bp + rec.receiving_be +
                                        rec.receiving_fs + rec.receiving_toi +
                                        rec.receiving_ft) / 7

    # FNZ Video Assessment

    overall_fnz = fields.Float(string="Overall FNZ",
                               compute="get_overall_fnz",
                               store=True, default=0)

    # FNZ TO FNK

    fnz_to_fnk = fields.Float(
        string="TO: Forehand net kill",
        compute="get_fnz_to_fnk",
        store=True, default=0)

    fnz_to_fnk_grip = fields.Integer(string="Grip", default=0)
    fnz_to_fnk_sp = fields.Integer(string="Starting Position", default=0)
    fnz_to_fnk_bp = fields.Integer(string="Backswing Position", default=0)
    fnz_to_fnk_be = fields.Integer(string="Backswing Endpoint", default=0)
    fnz_to_fnk_fs = fields.Integer(string="Forward Swing", default=0)
    fnz_to_fnk_toi = fields.Integer(string="Time of Impact", default=0)
    fnz_to_fnk_ft = fields.Integer(string="Follow Through", default=0)

    fnz_to_fnk_video = fields.Binary(string="TO: Forehand net kill video",
                                     attachment=True,
                                     copy=False)

    @api.depends('fnz_to_fnk_grip', 'fnz_to_fnk_sp', 'fnz_to_fnk_bp',
                 'fnz_to_fnk_be', 'fnz_to_fnk_fs', 'fnz_to_fnk_toi',
                 'fnz_to_fnk_ft')
    def get_fnz_to_fnk(self):
        for rec in self:
            rec.fnz_to_fnk = (rec.fnz_to_fnk_grip + rec.fnz_to_fnk_sp +
                              rec.fnz_to_fnk_bp + rec.fnz_to_fnk_be +
                              rec.fnz_to_fnk_fs + rec.fnz_to_fnk_toi +
                              rec.fnz_to_fnk_ft) / 7

    # FNZ CO FNP

    fnz_co_fnp = fields.Float(
        string="CO: Forehand net push",
        compute="get_fnz_co_fnp",
        store=True,
        default=0)

    fnz_co_fnp_grip = fields.Integer(string="Grip", default=0)
    fnz_co_fnp_sp = fields.Integer(
        string="Starting Position", default=0)
    fnz_co_fnp_bp = fields.Integer(
        string="Backswing Position", default=0)
    fnz_co_fnp_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fnz_co_fnp_fs = fields.Integer(
        string="Forward Swing", default=0)
    fnz_co_fnp_toi = fields.Integer(
        string="Time of Impact", default=0)
    fnz_co_fnp_ft = fields.Integer(
        string="Follow Through", default=0)

    fnz_co_fnp_video = fields.Binary(string="CO: Forehand net push video",
                                     attachment=True,
                                     copy=False)

    @api.depends('fnz_co_fnp_grip', 'fnz_co_fnp_sp', 'fnz_co_fnp_bp',
                 'fnz_co_fnp_be', 'fnz_co_fnp_fs', 'fnz_co_fnp_toi',
                 'fnz_co_fnp_ft')
    def get_fnz_co_fnp(self):
        for rec in self:
            rec.fnz_co_fnp = (rec.fnz_co_fnp_grip + rec.fnz_co_fnp_sp +
                              rec.fnz_co_fnp_bp + rec.fnz_co_fnp_be +
                              rec.fnz_co_fnp_fs + rec.fnz_co_fnp_toi +
                              rec.fnz_co_fnp_ft) / 7

    # FNZ CO OFCN

    fnz_co_ofcn = fields.Float(
        string="CO: Offensive forehand cross net",
        compute="get_fnz_co_ofcn",
        store=True,
        default=0)

    fnz_co_ofcn_grip = fields.Integer(string="Grip", default=0)
    fnz_co_ofcn_sp = fields.Integer(string="Starting Position", default=0)
    fnz_co_ofcn_bp = fields.Integer(string="Backswing Position", default=0)
    fnz_co_ofcn_be = fields.Integer(string="Backswing Endpoint", default=0)
    fnz_co_ofcn_fs = fields.Integer(string="Forward Swing", default=0)
    fnz_co_ofcn_toi = fields.Integer(string="Time of Impact", default=0)
    fnz_co_ofcn_ft = fields.Integer(string="Follow Through", default=0)

    fnz_co_ofcn_video = fields.Binary(
        string="CO: Offensive forehand cross net video",
        attachment=True,
        copy=False)

    @api.depends('fnz_co_ofcn_grip', 'fnz_co_ofcn_sp', 'fnz_co_ofcn_bp',
                 'fnz_co_ofcn_be', 'fnz_co_ofcn_fs', 'fnz_co_ofcn_toi',
                 'fnz_co_ofcn_ft')
    def get_fnz_co_ofcn(self):
        for rec in self:
            rec.fnz_co_ofcn = (rec.fnz_co_ofcn_grip + rec.fnz_co_ofcn_sp +
                               rec.fnz_co_ofcn_bp + rec.fnz_co_ofcn_be +
                               rec.fnz_co_ofcn_fs + rec.fnz_co_ofcn_toi +
                               rec.fnz_co_ofcn_ft) / 7

    # FNZ CO FOL

    fnz_co_fol = fields.Float(
        string="CO: Forehand offensive lift",
        compute="get_fnz_co_fol",
        store=True, default=0)

    fnz_co_fol_grip = fields.Integer(string="Grip", default=0)
    fnz_co_fol_sp = fields.Integer(string="Starting Position", default=0)
    fnz_co_fol_bp = fields.Integer(string="Backswing Position", default=0)
    fnz_co_fol_be = fields.Integer(string="Backswing Endpoint", default=0)
    fnz_co_fol_fs = fields.Integer(string="Forward Swing", default=0)
    fnz_co_fol_toi = fields.Integer(string="Time of Impact", default=0)
    fnz_co_fol_ft = fields.Integer(string="Follow Through", default=0)

    fnz_co_fol_video = fields.Binary(string="CO: Forehand offensive lift video",
                                     attachment=True,
                                     copy=False)

    @api.depends('fnz_co_fol_grip', 'fnz_co_fol_sp', 'fnz_co_fol_bp',
                 'fnz_co_fol_be', 'fnz_co_fol_fs', 'fnz_co_fol_toi',
                 'fnz_co_fol_ft')
    def get_fnz_co_fol(self):
        for rec in self:
            rec.fnz_co_fol = (rec.fnz_co_fol_grip + rec.fnz_co_fol_sp +
                              rec.fnz_co_fol_bp + rec.fnz_co_fol_be +
                              rec.fnz_co_fol_fs + rec.fnz_co_fol_toi +
                              rec.fnz_co_fol_ft) / 7

    # FNZ CO FSS

    fnz_co_fss = fields.Float(
        string="CO: Forehand straight spin",
        compute='get_fnz_co_fss',
        store=True, default=0)

    fnz_co_fss_grip = fields.Integer(string="Grip", default=0)
    fnz_co_fss_sp = fields.Integer(string="Starting Position", default=0)
    fnz_co_fss_bp = fields.Integer(string="Backswing Position", default=0)
    fnz_co_fss_be = fields.Integer(string="Backswing Endpoint", default=0)
    fnz_co_fss_fs = fields.Integer(string="Forward Swing", default=0)
    fnz_co_fss_toi = fields.Integer(string="Time of Impact", default=0)
    fnz_co_fss_ft = fields.Integer(string="Follow Through", default=0)

    fnz_co_fss_video = fields.Binary(string="CO: Forehand straight spin video",
                                     attachment=True,
                                     copy=False)

    @api.depends('fnz_co_fss_grip', 'fnz_co_fss_sp', 'fnz_co_fss_bp',
                 'fnz_co_fss_be', 'fnz_co_fss_fs', 'fnz_co_fss_toi',
                 'fnz_co_fss_ft')
    def get_fnz_co_fss(self):
        for rec in self:
            rec.fnz_co_fss = (rec.fnz_co_fss_grip + rec.fnz_co_fss_sp +
                              rec.fnz_co_fss_bp + rec.fnz_co_fss_be +
                              rec.fnz_co_fss_fs + rec.fnz_co_fss_toi +
                              rec.fnz_co_fss_ft) / 7

    # FNZ CO FRS

    fnz_co_frs = fields.Float(
        string="CO: Forehand reverse spin",
        compute="get_fnz_co_frs",
        store=True, default=0)

    fnz_co_frs_grip = fields.Integer(string="Grip", default=0)
    fnz_co_frs_sp = fields.Integer(string="Starting Position", default=0)
    fnz_co_frs_bp = fields.Integer(string="Backswing Position", default=0)
    fnz_co_frs_be = fields.Integer(string="Backswing Endpoint", default=0)
    fnz_co_frs_fs = fields.Integer(string="Forward Swing", default=0)
    fnz_co_frs_toi = fields.Integer(string="Time of Impact", default=0)
    fnz_co_frs_ft = fields.Integer(string="Follow Through", default=0)

    fnz_co_frs_video = fields.Binary(string="CO: Forehand reverse spin video",
                                     attachment=True,
                                     copy=False)

    @api.depends('fnz_co_frs_grip', 'fnz_co_frs_sp', 'fnz_co_frs_bp',
                 'fnz_co_frs_be', 'fnz_co_frs_fs', 'fnz_co_frs_toi',
                 'fnz_co_frs_ft')
    def get_fnz_co_frs(self):
        for rec in self:
            rec.fnz_co_frs = (rec.fnz_co_frs_grip + rec.fnz_co_frs_sp +
                              rec.fnz_co_frs_bp + rec.fnz_co_frs_be +
                              rec.fnz_co_frs_fs + rec.fnz_co_frs_toi +
                              rec.fnz_co_frs_ft) / 7

    # FNZ CO NB

    fnz_co_nb = fields.Float(
        string="50/50 to CO: Net block",
        compute="get_fnz_co_nb",
        store=True,
        default=0)

    fnz_co_nb_grip = fields.Integer(
        string="Grip", default=0)
    fnz_co_nb_sp = fields.Integer(
        string="Starting Position", default=0)
    fnz_co_nb_bp = fields.Integer(
        string="Backswing Position", default=0)
    fnz_co_nb_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fnz_co_nb_fs = fields.Integer(
        string="Forward Swing", default=0)
    fnz_co_nb_toi = fields.Integer(
        string="Time of Impact", default=0)
    fnz_co_nb_ft = fields.Integer(
        string="Follow Through", default=0)

    fnz_co_nb_video = fields.Binary(string="50/50 to CO: Net block video",
                                    attachment=True,
                                    copy=False)

    @api.depends('fnz_co_nb_grip', 'fnz_co_nb_sp', 'fnz_co_nb_bp',
                 'fnz_co_nb_be', 'fnz_co_nb_fs', 'fnz_co_nb_toi',
                 'fnz_co_nb_ft')
    def get_fnz_co_nb(self):
        for rec in self:
            rec.fnz_co_nb = (rec.fnz_co_nb_grip + rec.fnz_co_nb_sp +
                             rec.fnz_co_nb_bp + rec.fnz_co_nb_be +
                             rec.fnz_co_nb_fs + rec.fnz_co_nb_toi +
                             rec.fnz_co_nb_ft) / 7

    # FNZ FRS

    fnz_frs = fields.Float(
        string="50/50: Forehand reverse spin",
        compute="get_fnz_frs", store=True, default=0)

    fnz_frs_grip = fields.Integer(
        string="Grip", default=0)
    fnz_frs_sp = fields.Integer(
        string="Starting Position", default=0)
    fnz_frs_bp = fields.Integer(
        string="Backswing Position", default=0)
    fnz_frs_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fnz_frs_fs = fields.Integer(
        string="Forward Swing", default=0)
    fnz_frs_toi = fields.Integer(
        string="Time of Impact", default=0)
    fnz_frs_ft = fields.Integer(
        string="Follow Through", default=0)

    fnz_frs_video = fields.Binary(string="50/50: Forehand reverse spin video",
                                  attachment=True,
                                  copy=False)

    @api.depends('fnz_frs_grip', 'fnz_frs_sp', 'fnz_frs_bp',
                 'fnz_frs_be', 'fnz_frs_fs', 'fnz_frs_toi',
                 'fnz_frs_ft')
    def get_fnz_frs(self):
        for rec in self:
            rec.fnz_frs = (rec.fnz_frs_grip + rec.fnz_frs_sp +
                           rec.fnz_frs_bp + rec.fnz_frs_be +
                           rec.fnz_frs_fs + rec.fnz_frs_toi +
                           rec.fnz_frs_ft) / 7

    # FNZ NEUTRALISATION

    fnz_neutralisation = fields.Float(string="Neutralisation",
                                      compute="get_fnz_neutralisation",
                                      store=True, default=0)

    fnz_neutralisation_grip = fields.Integer(
        string="Grip", default=0)
    fnz_neutralisation_sp = fields.Integer(
        string="Starting Position", default=0)
    fnz_neutralisation_bp = fields.Integer(
        string="Backswing Position", default=0)
    fnz_neutralisation_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fnz_neutralisation_fs = fields.Integer(
        string="Forward Swing", default=0)
    fnz_neutralisation_toi = fields.Integer(
        string="Time of Impact", default=0)
    fnz_neutralisation_ft = fields.Integer(
        string="Follow Through", default=0)

    fnz_neutralisation_video = fields.Binary(string="Neutralisation video",
                                             attachment=True,
                                             copy=False)

    @api.depends('fnz_neutralisation_grip', 'fnz_neutralisation_sp',
                 'fnz_neutralisation_bp',
                 'fnz_neutralisation_be', 'fnz_neutralisation_fs',
                 'fnz_neutralisation_toi',
                 'fnz_neutralisation_ft')
    def get_fnz_neutralisation(self):
        for rec in self:
            rec.fnz_neutralisation = (
                     rec.fnz_neutralisation_grip + rec.fnz_neutralisation_sp +
                     rec.fnz_neutralisation_bp + rec.fnz_neutralisation_be +
                     rec.fnz_neutralisation_fs + rec.fnz_neutralisation_toi +
                     rec.fnz_neutralisation_ft) / 7

    # FNZ CD DFCN

    fnz_cd_dfcn = fields.Float(
        string="CD: Defensive forehand cross net",
        compute="get_fnz_cd_dfcn",
        store=True, default=0)

    fnz_cd_dfcn_grip = fields.Integer(
        string="Grip", default=0)
    fnz_cd_dfcn_sp = fields.Integer(
        string="Starting Position", default=0)
    fnz_cd_dfcn_bp = fields.Integer(
        string="Backswing Position", default=0)
    fnz_cd_dfcn_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fnz_cd_dfcn_fs = fields.Integer(
        string="Forward Swing", default=0)
    fnz_cd_dfcn_toi = fields.Integer(
        string="Time of Impact", default=0)
    fnz_cd_dfcn_ft = fields.Integer(
        string="Follow Through", default=0)

    fnz_cd_dfcn_video = fields.Binary(
        string="CD: Defensive forehand cross net video",
        attachment=True,
        copy=False)

    @api.depends('fnz_cd_dfcn_grip', 'fnz_cd_dfcn_sp',
                 'fnz_cd_dfcn_bp', 'fnz_cd_dfcn_be',
                 'fnz_cd_dfcn_fs', 'fnz_cd_dfcn_toi',
                 'fnz_cd_dfcn_ft')
    def get_fnz_cd_dfcn(self):
        for rec in self:
            rec.fnz_cd_dfcn = (
                 rec.fnz_cd_dfcn_grip + rec.fnz_cd_dfcn_sp +
                 rec.fnz_cd_dfcn_bp + rec.fnz_cd_dfcn_be +
                 rec.fnz_cd_dfcn_fs + rec.fnz_cd_dfcn_toi +
                 rec.fnz_cd_dfcn_ft) / 7

    # FNZ CD DFL

    fnz_cd_dfl = fields.Float(
        string="CD: Defensive forehand lifts",
        compute="get_fnz_cd_dfl", store=True,
        default=0)

    fnz_cd_dfl_grip = fields.Integer(
        string="Grip", default=0)
    fnz_cd_dfl_sp = fields.Integer(
        string="Starting Position", default=0)
    fnz_cd_dfl_bp = fields.Integer(
        string="Backswing Position", default=0)
    fnz_cd_dfl_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fnz_cd_dfl_fs = fields.Integer(
        string="Forward Swing", default=0)
    fnz_cd_dfl_toi = fields.Integer(
        string="Time of Impact", default=0)
    fnz_cd_dfl_ft = fields.Integer(
        string="Follow Through", default=0)

    fnz_cd_dfl_video = fields.Binary(
        string="CD: Defensive forehand lifts video",
        attachment=True,
        copy=False)

    @api.depends('fnz_cd_dfl_grip', 'fnz_cd_dfl_sp',
                 'fnz_cd_dfl_bp', 'fnz_cd_dfl_be',
                 'fnz_cd_dfl_fs', 'fnz_cd_dfl_toi',
                 'fnz_cd_dfl_ft')
    def get_fnz_cd_dfl(self):
        for rec in self:
            rec.fnz_cd_dfl = (
                      rec.fnz_cd_dfl_grip + rec.fnz_cd_dfl_sp +
                      rec.fnz_cd_dfl_bp + rec.fnz_cd_dfl_be +
                      rec.fnz_cd_dfl_fs + rec.fnz_cd_dfl_toi +
                      rec.fnz_cd_dfl_ft) / 7

    # FNZ TD DD

    fnz_td_dd = fields.Float(string="TD: Defensive dive",
                             compute="get_fnz_td_dd",
                             store=True, default=0)

    fnz_td_dd_grip = fields.Integer(
        string="Grip", default=0)
    fnz_td_dd_sp = fields.Integer(
        string="Starting Position", default=0)
    fnz_td_dd_bp = fields.Integer(
        string="Backswing Position", default=0)
    fnz_td_dd_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fnz_td_dd_fs = fields.Integer(
        string="Forward Swing", default=0)
    fnz_td_dd_toi = fields.Integer(
        string="Time of Impact", default=0)
    fnz_td_dd_ft = fields.Integer(
        string="Follow Through", default=0)

    fnz_td_dd_video = fields.Binary(string="TD: Defensive dive video",
                                    attachment=True,
                                    copy=False)

    @api.depends('fnz_td_dd_grip', 'fnz_td_dd_sp',
                 'fnz_td_dd_bp', 'fnz_td_dd_be',
                 'fnz_td_dd_fs', 'fnz_td_dd_toi',
                 'fnz_td_dd_ft')
    def get_fnz_td_dd(self):
        for rec in self:
            rec.fnz_td_dd = (
                         rec.fnz_td_dd_grip + rec.fnz_td_dd_sp +
                         rec.fnz_td_dd_bp + rec.fnz_td_dd_be +
                         rec.fnz_td_dd_fs + rec.fnz_td_dd_toi +
                         rec.fnz_td_dd_ft) / 7

    @api.depends('fnz_to_fnk', 'fnz_co_fnp', 'fnz_co_ofcn',
                 'fnz_co_fol', 'fnz_co_fss', 'fnz_co_frs',
                 'fnz_co_nb', 'fnz_frs', 'fnz_neutralisation',
                 'fnz_cd_dfcn', 'fnz_cd_dfl', 'fnz_td_dd')
    def get_overall_fnz(self):
        for rec in self:
            rec.overall_fnz = (rec.fnz_to_fnk + rec.fnz_co_fnp +
                               rec.fnz_co_ofcn + rec.fnz_co_fol +
                               rec.fnz_co_fss + rec.fnz_co_frs +
                               rec.fnz_co_nb + rec.fnz_frs +
                               rec.fnz_neutralisation + rec.fnz_cd_dfcn +
                               rec.fnz_cd_dfl + rec.fnz_td_dd) / 12

    # BNZ Video Assessment

    overall_bnz = fields.Float(string="Overall BNZ",
                               compute="get_overall_bnz",
                               store=True, default=0)

    # BMZ TO FNK

    bnz_to_fnk = fields.Float(
        string="TO: Forehand net kill",
        compute="get_bnz_to_fnk",
        store=True, default=0)

    bnz_to_fnk_grip = fields.Integer(
        string="Grip", default=0)
    bnz_to_fnk_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_to_fnk_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_to_fnk_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_to_fnk_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_to_fnk_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_to_fnk_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_to_fnk_video = fields.Binary(string="TO: Forehand net kill video",
                                     attachment=True,
                                     copy=False)

    @api.depends('bnz_to_fnk_grip', 'bnz_to_fnk_sp', 'bnz_to_fnk_bp',
                 'bnz_to_fnk_be', 'bnz_to_fnk_fs', 'bnz_to_fnk_toi',
                 'bnz_to_fnk_ft')
    def get_bnz_to_fnk(self):
        for rec in self:
            rec.bnz_to_fnk = (rec.bnz_to_fnk_grip + rec.bnz_to_fnk_sp +
                            rec.bnz_to_fnk_bp + rec.bnz_to_fnk_be +
                            rec.bnz_to_fnk_fs + rec.bnz_to_fnk_toi +
                            rec.bnz_to_fnk_ft) / 7

    # BNZ CO FNP

    bnz_co_fnp = fields.Float(
        string="CO: Forehand net push",
        compute="get_bnz_co_fnp",
        store=True, default=0)

    bnz_co_fnp_grip = fields.Integer(
        string="Grip", default=0)
    bnz_co_fnp_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_co_fnp_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_co_fnp_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_co_fnp_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_co_fnp_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_co_fnp_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_co_fnp_video = fields.Binary(string="CO: Forehand net push video",
                                     attachment=True,
                                     copy=False)

    @api.depends('bnz_co_fnp_grip', 'bnz_co_fnp_sp', 'bnz_co_fnp_bp',
                 'bnz_co_fnp_be', 'bnz_co_fnp_fs', 'bnz_co_fnp_toi',
                 'bnz_co_fnp_ft')
    def get_bnz_co_fnp(self):
        for rec in self:
            rec.bnz_co_fnp = (rec.bnz_co_fnp_grip + rec.bnz_co_fnp_sp +
                              rec.bnz_co_fnp_bp + rec.bnz_co_fnp_be +
                              rec.bnz_co_fnp_fs + rec.bnz_co_fnp_toi +
                              rec.bnz_co_fnp_ft) / 7

    # BNZ CO OFCN

    bnz_co_ofcn = fields.Float(
        string="CO: Offensive forehand cross net",
        compute="get_bnz_co_ofcn",
        store=True, default=0)

    bnz_co_ofcn_grip = fields.Integer(
        string="Grip", default=0)
    bnz_co_ofcn_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_co_ofcn_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_co_ofcn_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_co_ofcn_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_co_ofcn_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_co_ofcn_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_co_ofcn_video = fields.Binary(
        string="CO: Offensive forehand cross net video",
        attachment=True,
        copy=False)

    @api.depends('bnz_co_ofcn_grip', 'bnz_co_ofcn_sp', 'bnz_co_ofcn_bp',
                 'bnz_co_ofcn_be', 'bnz_co_ofcn_fs', 'bnz_co_ofcn_toi',
                 'bnz_co_ofcn_ft')
    def get_bnz_co_ofcn(self):
        for rec in self:
            rec.bnz_co_ofcn = (rec.bnz_co_ofcn_grip + rec.bnz_co_ofcn_sp +
                              rec.bnz_co_ofcn_bp + rec.bnz_co_ofcn_be +
                              rec.bnz_co_ofcn_fs + rec.bnz_co_ofcn_toi +
                              rec.bnz_co_ofcn_ft) / 7

    # BNZ CO FOL

    bnz_co_fol = fields.Float(
        string="CO: Forehand offensive lift",
        compute="get_bnz_co_fol",
        store=True, default=0)

    bnz_co_fol_grip = fields.Integer(
        string="Grip", default=0)
    bnz_co_fol_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_co_fol_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_co_fol_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_co_fol_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_co_fol_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_co_fol_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_co_fol_video = fields.Binary(string="CO: Forehand offensive lift video",
                                     attachment=True,
                                     copy=False)

    @api.depends('bnz_co_fol_grip', 'bnz_co_fol_sp', 'bnz_co_fol_bp',
                 'bnz_co_fol_be', 'bnz_co_fol_fs', 'bnz_co_fol_toi',
                 'bnz_co_fol_ft')
    def get_bnz_co_fol(self):
        for rec in self:
            rec.bnz_co_fol = (rec.bnz_co_fol_grip + rec.bnz_co_fol_sp +
                               rec.bnz_co_fol_bp + rec.bnz_co_fol_be +
                               rec.bnz_co_fol_fs + rec.bnz_co_fol_toi +
                               rec.bnz_co_fol_ft) / 7

    # BNZ CO FSS

    bnz_co_fss = fields.Float(
        string="CO: Forehand straight spin",
        compute="get_bnz_co_fss", store=True,
        default=0)

    bnz_co_fss_grip = fields.Integer(
        string="Grip", default=0)
    bnz_co_fss_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_co_fss_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_co_fss_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_co_fss_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_co_fss_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_co_fss_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_co_fss_video = fields.Binary(string="CO: Forehand straight spin video",
                                     attachment=True,
                                     copy=False)

    @api.depends('bnz_co_fss_grip', 'bnz_co_fss_sp', 'bnz_co_fss_bp',
                 'bnz_co_fss_be', 'bnz_co_fss_fs', 'bnz_co_fss_toi',
                 'bnz_co_fss_ft')
    def get_bnz_co_fss(self):
        for rec in self:
            rec.bnz_co_fss = (rec.bnz_co_fss_grip + rec.bnz_co_fss_sp +
                              rec.bnz_co_fss_bp + rec.bnz_co_fss_be +
                              rec.bnz_co_fss_fs + rec.bnz_co_fss_toi +
                              rec.bnz_co_fss_ft) / 7

    # BNZ CO FRS

    bnz_co_frs = fields.Float(
        string="CO: Forehand reverse spin",
        compute="get_bnz_co_frs", store=True,
        default=0)

    bnz_co_frs_grip = fields.Integer(
        string="Grip", default=0)
    bnz_co_frs_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_co_frs_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_co_frs_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_co_frs_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_co_frs_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_co_frs_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_co_frs_video = fields.Binary(string="CO: Forehand reverse spin video",
                                     attachment=True,
                                     copy=False)

    @api.depends('bnz_co_frs_grip', 'bnz_co_frs_sp', 'bnz_co_frs_bp',
                 'bnz_co_frs_be', 'bnz_co_frs_fs', 'bnz_co_frs_toi',
                 'bnz_co_frs_ft')
    def get_bnz_co_frs(self):
        for rec in self:
            rec.bnz_co_frs = (rec.bnz_co_frs_grip + rec.bnz_co_frs_sp +
                              rec.bnz_co_frs_bp + rec.bnz_co_frs_be +
                              rec.bnz_co_frs_fs + rec.bnz_co_frs_toi +
                              rec.bnz_co_frs_ft) / 7

    # BNZ CO NB

    bnz_co_nb = fields.Float(
        string="50/50 to CO: Net block",
        compute="get_bnz_co_nb",
        store=True, default=0)

    bnz_co_nb_grip = fields.Integer(
        string="Grip", default=0)
    bnz_co_nb_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_co_nb_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_co_nb_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_co_nb_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_co_nb_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_co_nb_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_co_nb_video = fields.Binary(string="50/50 to CO: Net block video",
                                    attachment=True,
                                    copy=False)

    @api.depends('bnz_co_nb_grip', 'bnz_co_nb_sp', 'bnz_co_nb_bp',
                 'bnz_co_nb_be', 'bnz_co_nb_fs', 'bnz_co_nb_toi',
                 'bnz_co_nb_ft')
    def get_bnz_co_nb(self):
        for rec in self:
            rec.bnz_co_nb = (rec.bnz_co_nb_grip + rec.bnz_co_nb_sp +
                              rec.bnz_co_nb_bp + rec.bnz_co_nb_be +
                              rec.bnz_co_nb_fs + rec.bnz_co_nb_toi +
                              rec.bnz_co_nb_ft) / 7

    # BNZ FRS

    bnz_frs = fields.Float(
        string="50/50: Forehand reverse spin",
        compute="get_bnz_frs", store=True, default=0)

    bnz_frs_grip = fields.Integer(
        string="Grip", default=0)
    bnz_frs_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_frs_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_frs_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_frs_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_frs_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_frs_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_frs_video = fields.Binary(string="50/50: Forehand reverse spin video",
                                  attachment=True,
                                  copy=False)

    @api.depends('bnz_frs_grip', 'bnz_frs_sp', 'bnz_frs_bp',
                 'bnz_frs_be', 'bnz_frs_fs', 'bnz_frs_toi',
                 'bnz_frs_ft')
    def get_bnz_frs(self):
        for rec in self:
            rec.bnz_frs = (rec.bnz_frs_grip + rec.bnz_frs_sp +
                         rec.bnz_frs_bp + rec.bnz_frs_be +
                         rec.bnz_frs_fs + rec.bnz_frs_toi +
                         rec.bnz_frs_ft) / 7

    # BNZ NEUTRALISATION

    bnz_neutralisation = fields.Float(
        string="Neutralisation",
        compute="get_bnz_neutralisation",
        default=0,
        store=True)

    bnz_neutralisation_grip = fields.Integer(
        string="Grip", default=0)
    bnz_neutralisation_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_neutralisation_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_neutralisation_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_neutralisation_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_neutralisation_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_neutralisation_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_neutralisation_video = fields.Binary(string="Neutralisation video",
                                             attachment=True,
                                             copy=False)

    @api.depends('bnz_neutralisation_grip', 'bnz_neutralisation_sp',
                 'bnz_neutralisation_bp', 'bnz_neutralisation_be',
                 'bnz_neutralisation_fs', 'bnz_neutralisation_toi',
                 'bnz_neutralisation_ft')
    def get_bnz_neutralisation(self):
        for rec in self:
            rec.bnz_neutralisation = (
                     rec.bnz_neutralisation_grip + rec.bnz_neutralisation_sp +
                     rec.bnz_neutralisation_bp + rec.bnz_neutralisation_be +
                     rec.bnz_neutralisation_fs + rec.bnz_neutralisation_toi +
                     rec.bnz_neutralisation_ft) / 7

    # BNZ CD DFCN

    bnz_cd_dfcn = fields.Float(
        string="CD: Defensive forehand cross net",
        compute="get_bnz_cd_dfcn",
        default=0, store=True)

    bnz_cd_dfcn_grip = fields.Integer(
        string="Grip", default=0)
    bnz_cd_dfcn_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_cd_dfcn_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_cd_dfcn_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_cd_dfcn_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_cd_dfcn_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_cd_dfcn_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_cd_dfcn_video = fields.Binary(
        string="CD: Defensive forehand cross net video",
        attachment=True,
        copy=False)

    @api.depends('bnz_cd_dfcn_grip', 'bnz_cd_dfcn_sp',
                 'bnz_cd_dfcn_bp', 'bnz_cd_dfcn_be',
                 'bnz_cd_dfcn_fs', 'bnz_cd_dfcn_toi',
                 'bnz_cd_dfcn_ft')
    def get_bnz_cd_dfcn(self):
        for rec in self:
            rec.bnz_cd_dfcn = (
                 rec.bnz_cd_dfcn_grip + rec.bnz_cd_dfcn_sp +
                 rec.bnz_cd_dfcn_bp + rec.bnz_cd_dfcn_be +
                 rec.bnz_cd_dfcn_fs + rec.bnz_cd_dfcn_toi +
                 rec.bnz_cd_dfcn_ft) / 7

    # BNZ CD DFL

    bnz_cd_dfl = fields.Float(
        string="CD: Defensive forehand lifts",
        compute="get_bnz_cd_dfl",
        store=True, default=0)

    bnz_cd_dfl_grip = fields.Integer(
        string="Grip", default=0)
    bnz_cd_dfl_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_cd_dfl_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_cd_dfl_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_cd_dfl_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_cd_dfl_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_cd_dfl_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_cd_dfl_video = fields.Binary(
        string="CD: Defensive forehand lifts video",
        attachment=True,
        copy=False)

    @api.depends('bnz_cd_dfl_grip', 'bnz_cd_dfl_sp',
                 'bnz_cd_dfl_bp', 'bnz_cd_dfl_be',
                 'bnz_cd_dfl_fs', 'bnz_cd_dfl_toi',
                 'bnz_cd_dfl_ft')
    def get_bnz_cd_dfl(self):
        for rec in self:
            rec.bnz_cd_dfl = (
              rec.bnz_cd_dfl_grip + rec.bnz_cd_dfl_sp +
              rec.bnz_cd_dfl_bp + rec.bnz_cd_dfl_be +
              rec.bnz_cd_dfl_fs + rec.bnz_cd_dfl_toi +
              rec.bnz_cd_dfl_ft) / 7

    # BNZ TD DD

    bnz_td_dd = fields.Float(string="TD: Defensive dive",
                             compute="get_bnz_td_dd",
                             store=True, default=0)

    bnz_td_dd_grip = fields.Integer(
        string="Grip", default=0)
    bnz_td_dd_sp = fields.Integer(
        string="Starting Position", default=0)
    bnz_td_dd_bp = fields.Integer(
        string="Backswing Position", default=0)
    bnz_td_dd_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bnz_td_dd_fs = fields.Integer(
        string="Forward Swing", default=0)
    bnz_td_dd_toi = fields.Integer(
        string="Time of Impact", default=0)
    bnz_td_dd_ft = fields.Integer(
        string="Follow Through", default=0)

    bnz_td_dd_video = fields.Binary(string="TD: Defensive dive video",
                                    attachment=True,
                                    copy=False)

    @api.depends('bnz_td_dd_grip', 'bnz_td_dd_sp',
                 'bnz_td_dd_bp', 'bnz_td_dd_be',
                 'bnz_td_dd_fs', 'bnz_td_dd_toi',
                 'bnz_td_dd_ft')
    def get_bnz_td_dd(self):
        for rec in self:
            rec.bnz_td_dd = (
                 rec.bnz_td_dd_grip + rec.bnz_td_dd_sp +
                 rec.bnz_td_dd_bp + rec.bnz_td_dd_be +
                 rec.bnz_td_dd_fs + rec.bnz_td_dd_toi +
                 rec.bnz_td_dd_ft) / 7

    @api.depends('bnz_to_fnk', 'bnz_co_fnp', 'bnz_co_ofcn', 'bnz_co_fol',
                 'bnz_co_fss', 'bnz_co_frs', 'bnz_co_nb', 'bnz_frs',
                 'bnz_neutralisation', 'bnz_cd_dfcn', 'bnz_cd_dfl',
                 'bnz_td_dd')
    def get_overall_bnz(self):
        for rec in self:
            rec.overall_bnz = (rec.bnz_to_fnk + rec.bnz_co_fnp +
                               rec.bnz_co_ofcn + rec.bnz_co_fol +
                               rec.bnz_co_fss + rec.bnz_co_frs +
                               rec.bnz_co_nb + rec.bnz_frs +
                               rec.bnz_neutralisation + rec.bnz_cd_dfcn +
                               rec.bnz_cd_dfl + rec.bnz_td_dd) / 12

    # FMZ Video Assessment

    overall_fmz = fields.Float(string="Overall FMZ",
                               compute='get_overall_fmz',
                               store=True, default=0)

    # FMZ CO SS

    fmz_co_ss = fields.Float(string="CO: Side smash",
                             compute='get_fmz_co_ss',
                             store=True,
                             default=0)

    fmz_co_ss_grip = fields.Integer(
        string="Grip", default=0)
    fmz_co_ss_sp = fields.Integer(
        string="Starting Position", default=0)
    fmz_co_ss_bp = fields.Integer(
        string="Backswing Position", default=0)
    fmz_co_ss_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fmz_co_ss_fs = fields.Integer(
        string="Forward Swing", default=0)
    fmz_co_ss_toi = fields.Integer(
        string="Time of Impact", default=0)
    fmz_co_ss_ft = fields.Integer(
        string="Follow Through", default=0)

    fmz_co_ss_video = fields.Binary(string="CO: Side smash video")

    @api.depends('fmz_co_ss_grip', 'fmz_co_ss_sp', 'fmz_co_ss_bp',
                 'fmz_co_ss_be', 'fmz_co_ss_fs', 'fmz_co_ss_toi',
                 'fmz_co_ss_ft')
    def get_fmz_co_ss(self):
        for rec in self:
            rec.fmz_co_ss = (rec.fmz_co_ss_grip + rec.fmz_co_ss_sp +
                              rec.fmz_co_ss_bp + rec.fmz_co_ss_be +
                              rec.fmz_co_ss_fs + rec.fmz_co_ss_toi +
                              rec.fmz_co_ss_ft) / 7

    # FMZ FMCP

    fmz_fmcp = fields.Float(
        string="50/50: Forehand mid-court push (straight & cross)",
        compute="get_fmz_fmcp",
        default=0, store=True)

    fmz_fmcp_grip = fields.Integer(
        string="Grip", default=0)
    fmz_fmcp_sp = fields.Integer(
        string="Starting Position", default=0)
    fmz_fmcp_bp = fields.Integer(
        string="Backswing Position", default=0)
    fmz_fmcp_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fmz_fmcp_fs = fields.Integer(
        string="Forward Swing", default=0)
    fmz_fmcp_toi = fields.Integer(
        string="Time of Impact", default=0)
    fmz_fmcp_ft = fields.Integer(
        string="Follow Through", default=0)

    fmz_fmcp_video = fields.Binary(
        string="50/50: Forehand mid-court push (straight & cross) video")

    @api.depends('fmz_fmcp_grip', 'fmz_fmcp_sp', 'fmz_fmcp_bp',
                 'fmz_fmcp_be', 'fmz_fmcp_fs', 'fmz_fmcp_toi',
                 'fmz_fmcp_ft')
    def get_fmz_fmcp(self):
        for rec in self:
            rec.fmz_fmcp = (rec.fmz_fmcp_grip + rec.fmz_fmcp_sp +
                             rec.fmz_fmcp_bp + rec.fmz_fmcp_be +
                             rec.fmz_fmcp_fs + rec.fmz_fmcp_toi +
                             rec.fmz_fmcp_ft) / 7

    # FMZ CD FDS S

    fmz_cd_fds_s = fields.Float(
        string="CD: Forehand defense straight (short)",
        default=0, store=True, compute="get_fmz_cd_fds_s")

    fmz_cd_fds_s_grip = fields.Integer(
        string="Grip", default=0)
    fmz_cd_fds_s_sp = fields.Integer(
        string="Starting Position", default=0)
    fmz_cd_fds_s_bp = fields.Integer(
        string="Backswing Position", default=0)
    fmz_cd_fds_s_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fmz_cd_fds_s_fs = fields.Integer(
        string="Forward Swing", default=0)
    fmz_cd_fds_s_toi = fields.Integer(
        string="Time of Impact", default=0)
    fmz_cd_fds_s_ft = fields.Integer(
        string="Follow Through", default=0)

    fmz_cd_fds_s_video = fields.Binary(
        string="CD: Forehand defense straight (short) video",
        default=0)

    @api.depends('fmz_cd_fds_s_grip', 'fmz_cd_fds_s_sp', 'fmz_cd_fds_s_bp',
                 'fmz_cd_fds_s_be', 'fmz_cd_fds_s_fs', 'fmz_cd_fds_s_toi',
                 'fmz_cd_fds_s_ft')
    def get_fmz_cd_fds_s(self):
        for rec in self:
            rec.fmz_cd_fds_s = (rec.fmz_cd_fds_s_grip + rec.fmz_cd_fds_s_sp +
                            rec.fmz_cd_fds_s_bp + rec.fmz_cd_fds_s_be +
                            rec.fmz_cd_fds_s_fs + rec.fmz_cd_fds_s_toi +
                            rec.fmz_cd_fds_s_ft) / 7

    # FMZ CD FDC S

    fmz_cd_fdc_s = fields.Float(
        string="CD: Forehand defense cross (short)",
        default=0, store=True, compute="get_fmz_cd_fdc_s")

    fmz_cd_fdc_s_grip = fields.Integer(
        string="Grip", default=0)
    fmz_cd_fdc_s_sp = fields.Integer(
        string="Starting Position", default=0)
    fmz_cd_fdc_s_bp = fields.Integer(
        string="Backswing Position", default=0)
    fmz_cd_fdc_s_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fmz_cd_fdc_s_fs = fields.Integer(
        string="Forward Swing", default=0)
    fmz_cd_fdc_s_toi = fields.Integer(
        string="Time of Impact", default=0)
    fmz_cd_fdc_s_ft = fields.Integer(
        string="Follow Through", default=0)

    fmz_cd_fdc_s_video = fields.Binary(
        string="CD: Forehand defense cross (short) video")

    @api.depends('fmz_cd_fdc_s_grip', 'fmz_cd_fdc_s_sp', 'fmz_cd_fdc_s_bp',
                 'fmz_cd_fdc_s_be', 'fmz_cd_fdc_s_fs', 'fmz_cd_fdc_s_toi',
                 'fmz_cd_fdc_s_ft')
    def get_fmz_cd_fdc_s(self):
        for rec in self:
            rec.fmz_cd_fdc_s = (rec.fmz_cd_fdc_s_grip + rec.fmz_cd_fdc_s_sp +
                              rec.fmz_cd_fdc_s_bp + rec.fmz_cd_fdc_s_be +
                              rec.fmz_cd_fdc_s_fs + rec.fmz_cd_fdc_s_toi +
                              rec.fmz_cd_fdc_s_ft) / 7

    # FMZ CD FDS L

    fmz_cd_fds_l = fields.Float(string="CD: Forehand defense straight (long)",
                                compute="get_fmz_cd_fds_l",
                                store=True, default=0)

    fmz_cd_fds_l_grip = fields.Integer(
        string="Grip", default=0)
    fmz_cd_fds_l_sp = fields.Integer(
        string="Starting Position", default=0)
    fmz_cd_fds_l_bp = fields.Integer(
        string="Backswing Position", default=0)
    fmz_cd_fds_l_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fmz_cd_fds_l_fs = fields.Integer(
        string="Forward Swing", default=0)
    fmz_cd_fds_l_toi = fields.Integer(
        string="Time of Impact", default=0)
    fmz_cd_fds_l_ft = fields.Integer(
        string="Follow Through", default=0)

    fmz_cd_fds_l_video = fields.Binary(
        string="CD: Forehand defense straight (long) video")

    @api.depends('fmz_cd_fds_l_grip', 'fmz_cd_fds_l_sp', 'fmz_cd_fds_l_bp',
                 'fmz_cd_fds_l_be', 'fmz_cd_fds_l_fs', 'fmz_cd_fds_l_toi',
                 'fmz_cd_fds_l_ft')
    def get_fmz_cd_fds_l(self):
        for rec in self:
            rec.fmz_cd_fds_l = (rec.fmz_cd_fds_l_grip + rec.fmz_cd_fds_l_sp +
                              rec.fmz_cd_fds_l_bp + rec.fmz_cd_fds_l_be +
                              rec.fmz_cd_fds_l_fs + rec.fmz_cd_fds_l_toi +
                              rec.fmz_cd_fds_l_ft) / 7

    # FMZ CD FDC L

    fmz_cd_fdc_l = fields.Float(
        string="CD: Forehand defense cross (long)",
        compute="get_fmz_cd_fdc_l", store=True, default=0)

    fmz_cd_fdc_l_grip = fields.Integer(
        string="Grip", default=0)
    fmz_cd_fdc_l_sp = fields.Integer(
        string="Starting Position", default=0)
    fmz_cd_fdc_l_bp = fields.Integer(
        string="Backswing Position", default=0)
    fmz_cd_fdc_l_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fmz_cd_fdc_l_fs = fields.Integer(
        string="Forward Swing", default=0)
    fmz_cd_fdc_l_toi = fields.Integer(
        string="Time of Impact", default=0)
    fmz_cd_fdc_l_ft = fields.Integer(
        string="Follow Through", default=0)

    fmz_cd_fdc_l_video = fields.Binary(
        string="CD: Forehand defense cross (long) video")

    @api.depends('fmz_cd_fdc_l_grip', 'fmz_cd_fdc_l_sp', 'fmz_cd_fdc_l_bp',
                 'fmz_cd_fdc_l_be', 'fmz_cd_fdc_l_fs', 'fmz_cd_fdc_l_toi',
                 'fmz_cd_fdc_l_ft')
    def get_fmz_cd_fdc_l(self):
        for rec in self:
            rec.fmz_cd_fdc_l = (rec.fmz_cd_fdc_l_grip + rec.fmz_cd_fdc_l_sp +
                              rec.fmz_cd_fdc_l_bp + rec.fmz_cd_fdc_l_be +
                              rec.fmz_cd_fdc_l_fs + rec.fmz_cd_fdc_l_toi +
                              rec.fmz_cd_fdc_l_ft) / 7

    # FMZ CD FDCA

    fmz_cd_fdca = fields.Float(
        string="CD: Forehand defense contra-attack",
        compute="get_fmz_cd_fdca", store=True, default=0)

    fmz_cd_fdca_grip = fields.Integer(
        string="Grip", default=0)
    fmz_cd_fdca_sp = fields.Integer(
        string="Starting Position", default=0)
    fmz_cd_fdca_bp = fields.Integer(
        string="Backswing Position", default=0)
    fmz_cd_fdca_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fmz_cd_fdca_fs = fields.Integer(
        string="Forward Swing", default=0)
    fmz_cd_fdca_toi = fields.Integer(
        string="Time of Impact", default=0)
    fmz_cd_fdca_ft = fields.Integer(
        string="Follow Through", default=0)

    fmz_cd_fdca_video = fields.Binary(
        string="CD: Forehand defense contra-attack video")

    @api.depends('fmz_cd_fdca_grip', 'fmz_cd_fdca_sp', 'fmz_cd_fdca_bp',
                 'fmz_cd_fdca_be', 'fmz_cd_fdca_fs', 'fmz_cd_fdca_toi',
                 'fmz_cd_fdca_ft')
    def get_fmz_cd_fdca(self):
        for rec in self:
            rec.fmz_cd_fdca = (rec.fmz_cd_fdca_grip + rec.fmz_cd_fdca_sp +
                               rec.fmz_cd_fdca_bp + rec.fmz_cd_fdca_be +
                               rec.fmz_cd_fdca_fs + rec.fmz_cd_fdca_toi +
                               rec.fmz_cd_fdca_ft) / 7

    # FM FD

    fmz_fd = fields.Float(string="TD: Forehand dive",
                          compute="get_fmz_fd",
                          store=True, default=0)

    fmz_fd_grip = fields.Integer(
        string="Grip", default=0)
    fmz_fd_sp = fields.Integer(
        string="Starting Position", default=0)
    fmz_fd_bp = fields.Integer(
        string="Backswing Position", default=0)
    fmz_fd_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    fmz_fd_fs = fields.Integer(
        string="Forward Swing", default=0)
    fmz_fd_toi = fields.Integer(
        string="Time of Impact", default=0)
    fmz_fd_ft = fields.Integer(
        string="Follow Through", default=0)

    fmz_fd_video = fields.Binary(string="TD: Forehand dive video")

    @api.depends('fmz_fd_grip', 'fmz_fd_sp', 'fmz_fd_bp',
                 'fmz_fd_be', 'fmz_fd_fs', 'fmz_fd_toi',
                 'fmz_fd_ft')
    def get_fmz_fd(self):
        for rec in self:
            rec.fmz_fd = (rec.fmz_fd_grip + rec.fmz_fd_sp +
                               rec.fmz_fd_bp + rec.fmz_fd_be +
                               rec.fmz_fd_fs + rec.fmz_fd_toi +
                               rec.fmz_fd_ft) / 7

    @api.depends('fmz_co_ss', 'fmz_fmcp', 'fmz_cd_fds_s',
                 'fmz_cd_fdc_s', 'fmz_cd_fds_l',
                 'fmz_cd_fdc_l', 'fmz_cd_fdca', 'fmz_fd')
    def get_overall_fmz(self):
        for rec in self:
            rec.overall_fmz = (rec.fmz_co_ss + rec.fmz_fmcp
                               + rec.fmz_cd_fds_s + rec.fmz_cd_fdc_s
                               + rec.fmz_cd_fds_l + rec.fmz_cd_fdc_l + rec.fmz_cd_fdca + rec.fmz_fd) / 8

    # BMZ video Assessment

    overall_bmz = fields.Integer(string="Overall BMZ",
                                 compute='get_overall_bmz',
                                 store=True, default=0)

    # BMZ CO SS

    bmz_co_ss = fields.Float(string="CO: Side smash",
                             compute="get_bmz_co_ss",
                             default=0,
                             store=True)

    bmz_co_ss_grip = fields.Integer(
        string="Grip", default=0)
    bmz_co_ss_sp = fields.Integer(
        string="Starting Position", default=0)
    bmz_co_ss_bp = fields.Integer(
        string="Backswing Position", default=0)
    bmz_co_ss_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bmz_co_ss_fs = fields.Integer(
        string="Forward Swing", default=0)
    bmz_co_ss_toi = fields.Integer(
        string="Time of Impact", default=0)
    bmz_co_ss_ft = fields.Integer(
        string="Follow Through", default=0)

    bmz_co_ss_video = fields.Binary(string="CO: Side smash video")

    @api.depends('bmz_co_ss_grip', 'bmz_co_ss_sp', 'bmz_co_ss_bp',
                 'bmz_co_ss_be', 'bmz_co_ss_fs', 'bmz_co_ss_toi',
                 'bmz_co_ss_ft')
    def get_bmz_co_ss(self):
        for rec in self:
            rec.bmz_co_ss = (rec.bmz_co_ss_grip + rec.bmz_co_ss_sp +
                             rec.bmz_co_ss_bp + rec.bmz_co_ss_be +
                             rec.bmz_co_ss_fs + rec.bmz_co_ss_toi +
                             rec.bmz_co_ss_ft) / 7

    # BMZ BMCP

    bmz_bmcp = fields.Float(
        string="50/50: Backhand mid-court push (straight & cross)",
        compute="get_bmz_bmcp", default=0, store=True)

    bmz_bmcp_grip = fields.Integer(
        string="Grip", default=0)
    bmz_bmcp_sp = fields.Integer(
        string="Starting Position", default=0)
    bmz_bmcp_bp = fields.Integer(
        string="Backswing Position", default=0)
    bmz_bmcp_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bmz_bmcp_fs = fields.Integer(
        string="Forward Swing", default=0)
    bmz_bmcp_toi = fields.Integer(
        string="Time of Impact", default=0)
    bmz_bmcp_ft = fields.Integer(
        string="Follow Through", default=0)

    bmz_bmcp_video = fields.Binary(
        string="50/50: Backhand mid-court push (straight & cross) video")

    @api.depends('bmz_bmcp_grip', 'bmz_bmcp_sp', 'bmz_bmcp_bp',
                 'bmz_bmcp_be', 'bmz_bmcp_fs', 'bmz_bmcp_toi',
                 'bmz_bmcp_ft')
    def get_bmz_bmcp(self):
        for rec in self:
            rec.bmz_bmcp = (rec.bmz_bmcp_grip + rec.bmz_bmcp_sp +
                             rec.bmz_bmcp_bp + rec.bmz_bmcp_be +
                             rec.bmz_bmcp_fs + rec.bmz_bmcp_toi +
                             rec.bmz_bmcp_ft) / 7

    # BMZ CD BDS S

    bmz_cd_bds_s = fields.Float(
        string="CD: Backhand defense straight (short)",
        compute="get_bmz_cd_bds_s",
        default=0, store=True)

    bmz_cd_bds_s_grip = fields.Integer(
        string="Grip", default=0)
    bmz_cd_bds_s_sp = fields.Integer(
        string="Starting Position", default=0)
    bmz_cd_bds_s_bp = fields.Integer(
        string="Backswing Position", default=0)
    bmz_cd_bds_s_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bmz_cd_bds_s_fs = fields.Integer(
        string="Forward Swing", default=0)
    bmz_cd_bds_s_toi = fields.Integer(
        string="Time of Impact", default=0)
    bmz_cd_bds_s_ft = fields.Integer(
        string="Follow Through", default=0)

    bmz_cd_bds_s_video = fields.Binary(
        string="CD: Backhand defense straight (short) video")

    @api.depends('bmz_cd_bds_s_grip', 'bmz_cd_bds_s_sp', 'bmz_cd_bds_s_bp',
                 'bmz_cd_bds_s_be', 'bmz_cd_bds_s_fs', 'bmz_cd_bds_s_toi',
                 'bmz_cd_bds_s_ft')
    def get_bmz_cd_bds_s(self):
        for rec in self:
            rec.bmz_cd_bds_s = (rec.bmz_cd_bds_s_grip + rec.bmz_cd_bds_s_sp +
                              rec.bmz_cd_bds_s_bp + rec.bmz_cd_bds_s_be +
                              rec.bmz_cd_bds_s_fs + rec.bmz_cd_bds_s_toi +
                              rec.bmz_cd_bds_s_ft) / 7

    # BMZ CD BDC S

    bmz_cd_bdc_s = fields.Float(
        string="CD: Backhand defense cross (short)",
        compute="get_bmz_cd_bdc_s", store=True, default=0)

    bmz_cd_bdc_s_grip = fields.Integer(
        string="Grip", default=0)
    bmz_cd_bdc_s_sp = fields.Integer(
        string="Starting Position", default=0)
    bmz_cd_bdc_s_bp = fields.Integer(
        string="Backswing Position", default=0)
    bmz_cd_bdc_s_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bmz_cd_bdc_s_fs = fields.Integer(
        string="Forward Swing", default=0)
    bmz_cd_bdc_s_toi = fields.Integer(
        string="Time of Impact", default=0)
    bmz_cd_bdc_s_ft = fields.Integer(
        string="Follow Through", default=0)

    bmz_cd_bdc_s_video = fields.Binary(
        string="CD: Backhand defense cross (short) video")

    @api.depends('bmz_cd_bdc_s_grip', 'bmz_cd_bdc_s_sp', 'bmz_cd_bdc_s_bp',
                 'bmz_cd_bdc_s_be', 'bmz_cd_bdc_s_fs', 'bmz_cd_bdc_s_toi',
                 'bmz_cd_bdc_s_ft')
    def get_bmz_cd_bdc_s(self):
        for rec in self:
            rec.bmz_cd_bdc_s = (rec.bmz_cd_bdc_s_grip + rec.bmz_cd_bdc_s_sp +
                              rec.bmz_cd_bdc_s_bp + rec.bmz_cd_bdc_s_be +
                              rec.bmz_cd_bdc_s_fs + rec.bmz_cd_bdc_s_toi +
                              rec.bmz_cd_bdc_s_ft) / 7

    # BMZ CD BDS L

    bmz_cd_bds_l = fields.Float(
        string="CD: Backhand defense straight (long)",
        compute="get_bmz_cd_bds_l", store=True, default=0)

    bmz_cd_bds_l_grip = fields.Integer(
        string="Grip", default=0)
    bmz_cd_bds_l_sp = fields.Integer(
        string="Starting Position", default=0)
    bmz_cd_bds_l_bp = fields.Integer(
        string="Backswing Position", default=0)
    bmz_cd_bds_l_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bmz_cd_bds_l_fs = fields.Integer(
        string="Forward Swing", default=0)
    bmz_cd_bds_l_toi = fields.Integer(
        string="Time of Impact", default=0)
    bmz_cd_bds_l_ft = fields.Integer(
        string="Follow Through", default=0)

    bmz_cd_bds_l_video = fields.Binary(
        string="CD: Backhand defense straight (long) video")

    @api.depends('bmz_cd_bds_l_grip', 'bmz_cd_bds_l_sp', 'bmz_cd_bds_l_bp',
                 'bmz_cd_bds_l_be', 'bmz_cd_bds_l_fs', 'bmz_cd_bds_l_toi',
                 'bmz_cd_bds_l_ft')
    def get_bmz_cd_bds_l(self):
        for rec in self:
            rec.bmz_cd_bds_l = (rec.bmz_cd_bds_l_grip + rec.bmz_cd_bds_l_sp +
                                rec.bmz_cd_bds_l_bp + rec.bmz_cd_bds_l_be +
                                rec.bmz_cd_bds_l_fs + rec.bmz_cd_bds_l_toi +
                                rec.bmz_cd_bds_l_ft) / 7

    # BMZ CD BDC L

    bmz_cd_bdc_l = fields.Float(
        string="CD: Backhand defense cross (long)",
        compute="get_bmz_cd_bdc_l", store=True, default=0)

    bmz_cd_bdc_l_grip = fields.Integer(
        string="Grip", default=0)
    bmz_cd_bdc_l_sp = fields.Integer(
        string="Starting Position", default=0)
    bmz_cd_bdc_l_bp = fields.Integer(
        string="Backswing Position", default=0)
    bmz_cd_bdc_l_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bmz_cd_bdc_l_fs = fields.Integer(
        string="Forward Swing", default=0)
    bmz_cd_bdc_l_toi = fields.Integer(
        string="Time of Impact", default=0)
    bmz_cd_bdc_l_ft = fields.Integer(
        string="Follow Through", default=0)

    bmz_cd_bdc_l_video = fields.Binary(
        string="CD: Backhand defense cross (long) video")

    @api.depends('bmz_cd_bdc_l_grip', 'bmz_cd_bdc_l_sp', 'bmz_cd_bdc_l_bp',
                 'bmz_cd_bdc_l_be', 'bmz_cd_bdc_l_fs', 'bmz_cd_bdc_l_toi',
                 'bmz_cd_bdc_l_ft')
    def get_bmz_cd_bdc_l(self):
        for rec in self:
            rec.bmz_cd_bdc_l = (rec.bmz_cd_bdc_l_grip + rec.bmz_cd_bdc_l_sp +
                                rec.bmz_cd_bdc_l_bp + rec.bmz_cd_bdc_l_be +
                                rec.bmz_cd_bdc_l_fs + rec.bmz_cd_bdc_l_toi +
                                rec.bmz_cd_bdc_l_ft) / 7

    # BMZ CD BDC

    bmz_cd_bdc = fields.Float(
        string="CD: Backhand defense contra-attack",
        compute="get_bmz_cd_bdc", default=0, store=True)

    bmz_cd_bdc_grip = fields.Integer(
        string="Grip", default=0)
    bmz_cd_bdc_sp = fields.Integer(
        string="Starting Position", default=0)
    bmz_cd_bdc_bp = fields.Integer(
        string="Backswing Position", default=0)
    bmz_cd_bdc_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bmz_cd_bdc_fs = fields.Integer(
        string="Forward Swing", default=0)
    bmz_cd_bdc_toi = fields.Integer(
        string="Time of Impact", default=0)
    bmz_cd_bdc_ft = fields.Integer(
        string="Follow Through", default=0)

    bmz_cd_bdc_video = fields.Binary(
        string="CD: Backhand defense contra-attack video")

    @api.depends('bmz_cd_bdc_grip', 'bmz_cd_bdc_sp', 'bmz_cd_bdc_bp',
                 'bmz_cd_bdc_be', 'bmz_cd_bdc_fs', 'bmz_cd_bdc_toi',
                 'bmz_cd_bdc_ft')
    def get_bmz_cd_bdc(self):
        for rec in self:
            rec.bmz_cd_bdc = (rec.bmz_cd_bdc_grip + rec.bmz_cd_bdc_sp +
                                rec.bmz_cd_bdc_bp + rec.bmz_cd_bdc_be +
                                rec.bmz_cd_bdc_fs + rec.bmz_cd_bdc_toi +
                                rec.bmz_cd_bdc_ft) / 7

    # BMZ TO BD
    bmz_td_bd = fields.Float(
        string="TD: Backhand dive",
        compute="get_bmz_td_bd",
        store=True, default=0)

    bmz_td_bd_grip = fields.Integer(
        string="Grip", default=0)
    bmz_td_bd_sp = fields.Integer(
        string="Starting Position", default=0)
    bmz_td_bd_bp = fields.Integer(
        string="Backswing Position", default=0)
    bmz_td_bd_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    bmz_td_bd_fs = fields.Integer(
        string="Forward Swing", default=0)
    bmz_td_bd_toi = fields.Integer(
        string="Time of Impact", default=0)
    bmz_td_bd_ft = fields.Integer(
        string="Follow Through", default=0)

    bmz_td_bd_video = fields.Binary(
        string="TD: Backhand dive video")

    @api.depends('bmz_td_bd_grip', 'bmz_td_bd_sp', 'bmz_td_bd_bp',
                 'bmz_td_bd_be', 'bmz_td_bd_fs', 'bmz_td_bd_toi',
                 'bmz_td_bd_ft')
    def get_bmz_td_bd(self):
        for rec in self:
            rec.bmz_td_bd = (rec.bmz_td_bd_grip + rec.bmz_td_bd_sp +
                                rec.bmz_td_bd_bp + rec.bmz_td_bd_be +
                                rec.bmz_td_bd_fs + rec.bmz_td_bd_toi +
                                rec.bmz_td_bd_ft) / 7

    @api.depends('bmz_co_ss', 'bmz_bmcp', 'bmz_cd_bds_s',
                 'bmz_cd_bdc_s', 'bmz_cd_bds_l',
                 'bmz_cd_bdc_l', 'bmz_cd_bdc', 'bmz_td_bd')
    def get_overall_bmz(self):
        for rec in self:
            rec.overall_bmz = (rec.bmz_co_ss + rec.bmz_bmcp
                               + rec.bmz_cd_bds_s + rec.bmz_cd_bdc_s
                               + rec.bmz_cd_bds_l + rec.bmz_cd_bdc_l + rec.bmz_cd_bdc + rec.bmz_td_bd) / 8

    # RCOvhz Video Assessment

    overall_rcovhz = fields.Float(string="Overall RCOvhz",
                                  compute="get_overall_rcovhz",
                                  default=0, store=True)

    # RCOVHZ TO JS

    rcovhz_to_js = fields.Float(string="TO: Jump smash",
                                compute="get_rcovhz_to_js",
                                store=True, default=0)

    rcovhz_to_js_grip = fields.Integer(
        string="Grip", default=0)
    rcovhz_to_js_sp = fields.Integer(
        string="Starting Position", default=0)
    rcovhz_to_js_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcovhz_to_js_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcovhz_to_js_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcovhz_to_js_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcovhz_to_js_ft = fields.Integer(
        string="Follow Through", default=0)

    rcovhz_to_js_video = fields.Binary(string="TO: Jump smash video")

    @api.depends('rcovhz_to_js_grip', 'rcovhz_to_js_sp', 'rcovhz_to_js_bp',
                 'rcovhz_to_js_be', 'rcovhz_to_js_fs', 'rcovhz_to_js_toi',
                 'rcovhz_to_js_ft')
    def get_rcovhz_to_js(self):
        for rec in self:
            rec.rcovhz_to_js = (rec.rcovhz_to_js_grip + rec.rcovhz_to_js_sp +
                                rec.rcovhz_to_js_bp + rec.rcovhz_to_js_be +
                                rec.rcovhz_to_js_fs + rec.rcovhz_to_js_toi +
                                rec.rcovhz_to_js_ft) / 7

    # RCOVHZ TO FRS

    rcovhz_to_frs = fields.Float(
        string="TO: Full-body rotation smash",
        compute="get_rcovhz_to_frs",
        default=0, store=True)

    rcovhz_to_frs_grip = fields.Integer(
        string="Grip", default=0)
    rcovhz_to_frs_sp = fields.Integer(
        string="Starting Position", default=0)
    rcovhz_to_frs_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcovhz_to_frs_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcovhz_to_frs_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcovhz_to_frs_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcovhz_to_frs_ft = fields.Integer(
        string="Follow Through", default=0)

    rcovhz_to_frs_video = fields.Binary(
        string="TO: Full-body rotation smash video")

    @api.depends('rcovhz_to_frs_grip', 'rcovhz_to_frs_sp', 'rcovhz_to_frs_bp',
                 'rcovhz_to_frs_be', 'rcovhz_to_frs_fs', 'rcovhz_to_frs_toi',
                 'rcovhz_to_frs_ft')
    def get_rcovhz_to_frs(self):
        for rec in self:
            rec.rcovhz_to_frs = (rec.rcovhz_to_frs_grip + rec.rcovhz_to_frs_sp +
                                rec.rcovhz_to_frs_bp + rec.rcovhz_to_frs_be +
                                rec.rcovhz_to_frs_fs + rec.rcovhz_to_frs_toi +
                                rec.rcovhz_to_frs_ft) / 7

    # RCOVHZ TO CO SS

    rcovhz_to_co_ss = fields.Float(
        string="TO to CO: Stick smash",
        compute="get_rcovhz_to_co_ss",
        default=0, store=True)

    rcovhz_to_co_ss_grip = fields.Integer(
        string="Grip", default=0)
    rcovhz_to_co_ss_sp = fields.Integer(
        string="Starting Position", default=0)
    rcovhz_to_co_ss_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcovhz_to_co_ss_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcovhz_to_co_ss_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcovhz_to_co_ss_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcovhz_to_co_ss_ft = fields.Integer(
        string="Follow Through", default=0)

    rcovhz_to_co_ss_video = fields.Binary(
        string="TO to CO: Stick smash video")

    @api.depends('rcovhz_to_co_ss_grip', 'rcovhz_to_co_ss_sp', 'rcovhz_to_co_ss_bp',
                 'rcovhz_to_co_ss_be', 'rcovhz_to_co_ss_fs', 'rcovhz_to_co_ss_toi',
                 'rcovhz_to_co_ss_ft')
    def get_rcovhz_to_co_ss(self):
        for rec in self:
            rec.rcovhz_to_co_ss = (rec.rcovhz_to_co_ss_grip + rec.rcovhz_to_co_ss_sp +
                                rec.rcovhz_to_co_ss_bp + rec.rcovhz_to_co_ss_be +
                                rec.rcovhz_to_co_ss_fs + rec.rcovhz_to_co_ss_toi +
                                rec.rcovhz_to_co_ss_ft) / 7

    # RCOVHZ CO CC

    rcovhz_co_oc = fields.Float(string="CO: Overhead cut",
                                compute="get_rcovhz_co_oc",
                                default=0, store=True)

    rcovhz_co_oc_grip = fields.Integer(
        string="Grip", default=0)
    rcovhz_co_oc_sp = fields.Integer(
        string="Starting Position", default=0)
    rcovhz_co_oc_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcovhz_co_oc_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcovhz_co_oc_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcovhz_co_oc_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcovhz_co_oc_ft = fields.Integer(
        string="Follow Through", default=0)

    rcovhz_co_oc_video = fields.Binary(
        string="CO: Overhead cut video")

    @api.depends('rcovhz_co_oc_grip', 'rcovhz_co_oc_sp', 'rcovhz_co_oc_bp',
                 'rcovhz_co_oc_be', 'rcovhz_co_oc_fs', 'rcovhz_co_oc_toi',
                 'rcovhz_co_oc_ft')
    def get_rcovhz_co_oc(self):
        for rec in self:
            rec.rcovhz_co_oc = (rec.rcovhz_co_oc_grip + rec.rcovhz_co_oc_sp +
                                rec.rcovhz_co_oc_bp + rec.rcovhz_co_oc_be +
                                rec.rcovhz_co_oc_fs + rec.rcovhz_co_oc_toi +
                                rec.rcovhz_co_oc_ft) / 7

    # RCOVHZ CO ORC

    rcovhz_co_orc = fields.Float(
        string="CO: Overhead reverse cut",
        compute="get_rcovhz_co_orc",
        default=0, store=True)

    rcovhz_co_orc_grip = fields.Integer(
        string="Grip", default=0)
    rcovhz_co_orc_sp = fields.Integer(
        string="Starting Position", default=0)
    rcovhz_co_orc_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcovhz_co_orc_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcovhz_co_orc_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcovhz_co_orc_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcovhz_co_orc_ft = fields.Integer(
        string="Follow Through", default=0)

    rcovhz_co_orc_video = fields.Binary(
        string="CO: Overhead reverse cut video")

    @api.depends('rcovhz_co_orc_grip', 'rcovhz_co_orc_sp', 'rcovhz_co_orc_bp',
                 'rcovhz_co_orc_be', 'rcovhz_co_orc_fs', 'rcovhz_co_orc_toi',
                 'rcovhz_co_orc_ft')
    def get_rcovhz_co_orc(self):
        for rec in self:
            rec.rcovhz_co_orc = (rec.rcovhz_co_orc_grip + rec.rcovhz_co_orc_sp +
                                rec.rcovhz_co_orc_bp + rec.rcovhz_co_orc_be +
                                rec.rcovhz_co_orc_fs + rec.rcovhz_co_orc_toi +
                                rec.rcovhz_co_orc_ft) / 7

    # RCOVHZ CO OOC

    rcovhz_co_ooc = fields.Float(
        string="CO: Overhead offensive clears",
        compute="get_rcovhz_co_ooc",
        default=0, store=True)

    rcovhz_co_ooc_grip = fields.Integer(
        string="Grip", default=0)
    rcovhz_co_ooc_sp = fields.Integer(
        string="Starting Position", default=0)
    rcovhz_co_ooc_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcovhz_co_ooc_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcovhz_co_ooc_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcovhz_co_ooc_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcovhz_co_ooc_ft = fields.Integer(
        string="Follow Through", default=0)

    rcovhz_co_ooc_video = fields.Binary(
        string="CO: Overhead offensive clears video")

    @api.depends('rcovhz_co_ooc_grip', 'rcovhz_co_ooc_sp', 'rcovhz_co_ooc_bp',
                 'rcovhz_co_ooc_be', 'rcovhz_co_ooc_fs', 'rcovhz_co_ooc_toi',
                 'rcovhz_co_ooc_ft')
    def get_rcovhz_co_ooc(self):
        for rec in self:
            rec.rcovhz_co_ooc = (rec.rcovhz_co_ooc_grip + rec.rcovhz_co_ooc_sp +
                                rec.rcovhz_co_ooc_bp + rec.rcovhz_co_ooc_be +
                                rec.rcovhz_co_ooc_fs + rec.rcovhz_co_ooc_toi +
                                rec.rcovhz_co_ooc_ft) / 7

    # RCOVHZ OC

    rcovhz_oc = fields.Float(
        string="50/50: Overhead clears",
        compute="get_rcovhz_oc",
        default=0, store=True)

    rcovhz_oc_grip = fields.Integer(
        string="Grip", default=0)
    rcovhz_oc_sp = fields.Integer(
        string="Starting Position", default=0)
    rcovhz_oc_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcovhz_oc_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcovhz_oc_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcovhz_oc_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcovhz_oc_ft = fields.Integer(
        string="Follow Through", default=0)

    rcovhz_oc_video = fields.Binary(
        string="50/50: Overhead clears video")

    @api.depends('rcovhz_oc_grip', 'rcovhz_oc_sp', 'rcovhz_oc_bp',
                 'rcovhz_oc_be', 'rcovhz_oc_fs', 'rcovhz_oc_toi',
                 'rcovhz_oc_ft')
    def get_rcovhz_oc(self):
        for rec in self:
            rec.rcovhz_oc = (rec.rcovhz_oc_grip + rec.rcovhz_oc_sp +
                                rec.rcovhz_oc_bp + rec.rcovhz_oc_be +
                                rec.rcovhz_oc_fs + rec.rcovhz_oc_toi +
                                rec.rcovhz_oc_ft) / 7

    @api.depends('rcovhz_to_js', 'rcovhz_to_frs', 'rcovhz_to_co_ss',
                 'rcovhz_co_oc',
                 'rcovhz_co_orc', 'rcovhz_co_ooc', 'rcovhz_oc')
    def get_overall_rcovhz(self):
        for rec in self:
            rec.overall_rcovhz = (rec.rcovhz_to_js + rec.rcovhz_to_frs
                                  + rec.rcovhz_to_co_ss + rec.rcovhz_co_oc
                                  + rec.rcovhz_co_orc + rec.rcovhz_co_ooc + rec.rcovhz_oc) / 7

    # RCBZ Video Assessment

    overall_rcbz = fields.Float(string="Overall RCBZ",
                                compute="get_overall_rcbz",
                                store=True, default=0)

    # RCBZ CO OBC

    rcbz_co_obc = fields.Float(
        string="CO: Offensive backhand clear",
        compute="get_rcbz_co_obc",
        default=0, store=True)

    rcbz_co_obc_grip = fields.Integer(
        string="Grip", default=0)
    rcbz_co_obc_sp = fields.Integer(
        string="Starting Position", default=0)
    rcbz_co_obc_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcbz_co_obc_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcbz_co_obc_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcbz_co_obc_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcbz_co_obc_ft = fields.Integer(
        string="Follow Through", default=0)

    rcbz_co_obc_video = fields.Binary(
        string="CO: Offensive backhand clear video")

    @api.depends('rcbz_co_obc_grip', 'rcbz_co_obc_sp', 'rcbz_co_obc_bp',
                 'rcbz_co_obc_be', 'rcbz_co_obc_fs', 'rcbz_co_obc_toi',
                 'rcbz_co_obc_ft')
    def get_rcbz_co_obc(self):
        for rec in self:
            rec.rcbz_co_obc = (rec.rcbz_co_obc_grip + rec.rcbz_co_obc_sp +
                                rec.rcbz_co_obc_bp + rec.rcbz_co_obc_be +
                                rec.rcbz_co_obc_fs + rec.rcbz_co_obc_toi +
                                rec.rcbz_co_obc_ft) / 7

    # RCBZ CO BRD

    rcbz_co_brd = fields.Float(
        string="CO: Backhand reverse drop",
        compute="get_rcbz_co_brd",
        default=0, store=True)

    rcbz_co_brd_grip = fields.Integer(
        string="Grip", default=0)
    rcbz_co_brd_sp = fields.Integer(
        string="Starting Position", default=0)
    rcbz_co_brd_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcbz_co_brd_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcbz_co_brd_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcbz_co_brd_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcbz_co_brd_ft = fields.Integer(
        string="Follow Through", default=0)

    rcbz_co_brd_video = fields.Binary(
        string="CO: Backhand reverse drop video")

    @api.depends('rcbz_co_brd_grip', 'rcbz_co_brd_sp', 'rcbz_co_brd_bp',
                 'rcbz_co_brd_be', 'rcbz_co_brd_fs', 'rcbz_co_brd_toi',
                 'rcbz_co_brd_ft')
    def get_rcbz_co_brd(self):
        for rec in self:
            rec.rcbz_co_brd = (rec.rcbz_co_brd_grip + rec.rcbz_co_brd_sp +
                                rec.rcbz_co_brd_bp + rec.rcbz_co_brd_be +
                                rec.rcbz_co_brd_fs + rec.rcbz_co_brd_toi +
                                rec.rcbz_co_brd_ft) / 7

    # RCBZ BCD

    rcbz_bcd = fields.Float(
        string="CO: Backhand cut drop",
        compute="get_rcbz_bcd",
        store=True, default=0)

    rcbz_bcd_grip = fields.Integer(
        string="Grip", default=0)
    rcbz_bcd_sp = fields.Integer(
        string="Starting Position", default=0)
    rcbz_bcd_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcbz_bcd_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcbz_bcd_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcbz_bcd_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcbz_bcd_ft = fields.Integer(
        string="Follow Through", default=0)

    rcbz_bcd_video = fields.Binary(
        string="CO: Backhand cut drop video")

    @api.depends('rcbz_bcd_grip', 'rcbz_bcd_sp', 'rcbz_bcd_bp',
                 'rcbz_bcd_be', 'rcbz_bcd_fs', 'rcbz_bcd_toi',
                 'rcbz_bcd_ft')
    def get_rcbz_bcd(self):
        for rec in self:
            rec.rcbz_bcd = (rec.rcbz_bcd_grip + rec.rcbz_bcd_sp +
                                rec.rcbz_bcd_bp + rec.rcbz_bcd_be +
                                rec.rcbz_bcd_fs + rec.rcbz_bcd_toi +
                                rec.rcbz_bcd_ft) / 7

    # RCBZ CD NS

    rcbz_cd_ns = fields.Float(
        string="50/50 to CD: Neutralisation straight",
        compute="get_rcbz_cd_ns",
        default=0, store=True)

    rcbz_cd_ns_grip = fields.Integer(
        string="Grip", default=0)
    rcbz_cd_ns_sp = fields.Integer(
        string="Starting Position", default=0)
    rcbz_cd_ns_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcbz_cd_ns_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcbz_cd_ns_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcbz_cd_ns_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcbz_cd_ns_ft = fields.Integer(
        string="Follow Through", default=0)

    rcbz_cd_ns_video = fields.Binary(
        string="50/50 to CD: Neutralisation straight video")

    @api.depends('rcbz_cd_ns_grip', 'rcbz_cd_ns_sp', 'rcbz_cd_ns_bp',
                 'rcbz_cd_ns_be', 'rcbz_cd_ns_fs', 'rcbz_cd_ns_toi',
                 'rcbz_cd_ns_ft')
    def get_rcbz_cd_ns(self):
        for rec in self:
            rec.rcbz_cd_ns = (rec.rcbz_cd_ns_grip + rec.rcbz_cd_ns_sp +
                                rec.rcbz_cd_ns_bp + rec.rcbz_cd_ns_be +
                                rec.rcbz_cd_ns_fs + rec.rcbz_cd_ns_toi +
                                rec.rcbz_cd_ns_ft) / 7

    # RCBZ CD NC

    rcbz_cd_nc = fields.Float(
        string="50/50 to CD: Neutralisation cross",
        compute="get_rcbz_cd_nc",
        default=0, store=True)

    rcbz_cd_nc_grip = fields.Integer(
        string="Grip", default=0)
    rcbz_cd_nc_sp = fields.Integer(
        string="Starting Position", default=0)
    rcbz_cd_nc_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcbz_cd_nc_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcbz_cd_nc_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcbz_cd_nc_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcbz_cd_nc_ft = fields.Integer(
        string="Follow Through", default=0)

    rcbz_cd_nc_video = fields.Binary(
        string="50/50 to CD: Neutralisation cross video")

    @api.depends('rcbz_cd_nc_grip', 'rcbz_cd_nc_sp', 'rcbz_cd_nc_bp',
                 'rcbz_cd_nc_be', 'rcbz_cd_nc_fs', 'rcbz_cd_nc_toi',
                 'rcbz_cd_nc_ft')
    def get_rcbz_cd_nc(self):
        for rec in self:
            rec.rcbz_cd_nc = (rec.rcbz_cd_nc_grip + rec.rcbz_cd_nc_sp +
                                rec.rcbz_cd_nc_bp + rec.rcbz_cd_nc_be +
                                rec.rcbz_cd_nc_fs + rec.rcbz_cd_nc_toi +
                                rec.rcbz_cd_nc_ft) / 7

    @api.depends('rcbz_co_obc', 'rcbz_co_brd', 'rcbz_bcd', 'rcbz_cd_ns',
                 'rcbz_cd_nc')
    def get_overall_rcbz(self):
        for assessment in self:
            assessment.overall_rcbz = (assessment.rcbz_co_obc +
                                       assessment.rcbz_co_brd +
                                       assessment.rcbz_bcd +
                                       assessment.rcbz_cd_ns +
                                       assessment.rcbz_cd_nc
                                       ) / 5

    # RCFZ Video Assessment

    overall_rcfz = fields.Float(string="Overall RCFZ",
                                compute="get_overall_rcfz",
                                store=True, default=0)

    # RCFZ TO JS

    rcfz_to_js = fields.Float(string="TO: Jump smash",
                              compute="get_rcfz_to_js",
                              default=0, store=True)

    rcfz_to_js_grip = fields.Integer(
        string="Grip", default=0)
    rcfz_to_js_sp = fields.Integer(
        string="Starting Position", default=0)
    rcfz_to_js_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcfz_to_js_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcfz_to_js_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcfz_to_js_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcfz_to_js_ft = fields.Integer(
        string="Follow Through", default=0)

    rcfz_to_js_video = fields.Binary(string="TO: Jump smash video")

    @api.depends('rcfz_to_js_grip', 'rcfz_to_js_sp', 'rcfz_to_js_bp',
                 'rcfz_to_js_be', 'rcfz_to_js_fs', 'rcfz_to_js_toi',
                 'rcfz_to_js_ft')
    def get_rcfz_to_js(self):
        for rec in self:
            rec.rcfz_to_js = (rec.rcfz_to_js_grip + rec.rcfz_to_js_sp +
                                rec.rcfz_to_js_bp + rec.rcfz_to_js_be +
                                rec.rcfz_to_js_fs + rec.rcfz_to_js_toi +
                                rec.rcfz_to_js_ft) / 7

    # RCFZ TO FBRS

    rcfz_to_fbrs = fields.Float(
        string="TO: Full body rotation smash",
        compute="get_rcfz_to_fbrs",
        default=0, store=True)

    rcfz_to_fbrs_grip = fields.Integer(
        string="Grip", default=0)
    rcfz_to_fbrs_sp = fields.Integer(
        string="Starting Position", default=0)
    rcfz_to_fbrs_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcfz_to_fbrs_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcfz_to_fbrs_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcfz_to_fbrs_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcfz_to_fbrs_ft = fields.Integer(
        string="Follow Through", default=0)

    rcfz_to_fbrs_video = fields.Binary(
        string="TO: Full body rotation smash video")

    @api.depends('rcfz_to_fbrs_grip', 'rcfz_to_fbrs_sp', 'rcfz_to_fbrs_bp',
                 'rcfz_to_fbrs_be', 'rcfz_to_fbrs_fs', 'rcfz_to_fbrs_toi',
                 'rcfz_to_fbrs_ft')
    def get_rcfz_to_fbrs(self):
        for rec in self:
            rec.rcfz_to_fbrs = (rec.rcfz_to_fbrs_grip + rec.rcfz_to_fbrs_sp +
                                rec.rcfz_to_fbrs_bp + rec.rcfz_to_fbrs_be +
                                rec.rcfz_to_fbrs_fs + rec.rcfz_to_fbrs_toi +
                                rec.rcfz_to_fbrs_ft) / 7

    # RCFZ CO OC

    rcfz_co_oc = fields.Float(string="CO: Offensive clears",
                              compute="get_rcfz_co_oc",
                              default=0, store=True)

    rcfz_co_oc_grip = fields.Integer(
        string="Grip", default=0)
    rcfz_co_oc_sp = fields.Integer(
        string="Starting Position", default=0)
    rcfz_co_oc_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcfz_co_oc_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcfz_co_oc_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcfz_co_oc_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcfz_co_oc_ft = fields.Integer(
        string="Follow Through", default=0)

    rcfz_co_oc_video = fields.Binary(string="CO: Offensive clears video")

    @api.depends('rcfz_co_oc_grip', 'rcfz_co_oc_sp', 'rcfz_co_oc_bp',
                 'rcfz_co_oc_be', 'rcfz_co_oc_fs', 'rcfz_co_oc_toi',
                 'rcfz_co_oc_ft')
    def get_rcfz_co_oc(self):
        for rec in self:
            rec.rcfz_co_oc = (rec.rcfz_co_oc_grip + rec.rcfz_co_oc_sp +
                                rec.rcfz_co_oc_bp + rec.rcfz_co_oc_be +
                                rec.rcfz_co_oc_fs + rec.rcfz_co_oc_toi +
                                rec.rcfz_co_oc_ft) / 7

    # RCFZ CO FCS

    rcfz_co_fcs = fields.Float(string="CO: Forehand cut straight",
                               compute="get_rcfz_co_fcs",
                               store=True,
                               default=0)

    rcfz_co_fcs_grip = fields.Integer(
        string="Grip", default=0)
    rcfz_co_fcs_sp = fields.Integer(
        string="Starting Position", default=0)
    rcfz_co_fcs_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcfz_co_fcs_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcfz_co_fcs_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcfz_co_fcs_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcfz_co_fcs_ft = fields.Integer(
        string="Follow Through", default=0)

    rcfz_co_fcs_video = fields.Binary(string="CO: Forehand cut straight video")

    @api.depends('rcfz_co_fcs_grip', 'rcfz_co_fcs_sp', 'rcfz_co_fcs_bp',
                 'rcfz_co_fcs_be', 'rcfz_co_fcs_fs', 'rcfz_co_fcs_toi',
                 'rcfz_co_fcs_ft')
    def get_rcfz_co_fcs(self):
        for rec in self:
            rec.rcfz_co_fcs = (rec.rcfz_co_fcs_grip + rec.rcfz_co_fcs_sp +
                                rec.rcfz_co_fcs_bp + rec.rcfz_co_fcs_be +
                                rec.rcfz_co_fcs_fs + rec.rcfz_co_fcs_toi +
                                rec.rcfz_co_fcs_ft) / 7

    # RCFZ TO FCC

    rcfz_co_fcc = fields.Float(string="CO: Forehand cut cross",
                               compute="get_rcfz_co_fcc",
                               default=0, store=True)

    rcfz_co_fcc_grip = fields.Integer(
        string="Grip", default=0)
    rcfz_co_fcc_sp = fields.Integer(
        string="Starting Position", default=0)
    rcfz_co_fcc_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcfz_co_fcc_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcfz_co_fcc_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcfz_co_fcc_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcfz_co_fcc_ft = fields.Integer(
        string="Follow Through", default=0)

    rcfz_co_fcc_video = fields.Binary(string="CO: Forehand cut cross video")

    @api.depends('rcfz_co_fcc_grip', 'rcfz_co_fcc_sp', 'rcfz_co_fcc_bp',
                 'rcfz_co_fcc_be', 'rcfz_co_fcc_fs', 'rcfz_co_fcc_toi',
                 'rcfz_co_fcc_ft')
    def get_rcfz_co_fcc(self):
        for rec in self:
            rec.rcfz_co_fcc = (rec.rcfz_co_fcc_grip + rec.rcfz_co_fcc_sp +
                                rec.rcfz_co_fcc_bp + rec.rcfz_co_fcc_be +
                                rec.rcfz_co_fcc_fs + rec.rcfz_co_fcc_toi +
                                rec.rcfz_co_fcc_ft) / 7

    # RCFZ CO FND

    rcfz_co_fnd = fields.Float(string="CO: Forehand normal drops",
                               compute="get_rcfz_co_fnd",
                               store=0, default=0)

    rcfz_co_fnd_grip = fields.Integer(
        string="Grip", default=0)
    rcfz_co_fnd_sp = fields.Integer(
        string="Starting Position", default=0)
    rcfz_co_fnd_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcfz_co_fnd_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcfz_co_fnd_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcfz_co_fnd_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcfz_co_fnd_ft = fields.Integer(
        string="Follow Through", default=0)

    rcfz_co_fnd_video = fields.Binary(string="CO: Forehand normal drops video")

    @api.depends('rcfz_co_fnd_grip', 'rcfz_co_fnd_sp', 'rcfz_co_fnd_bp',
                 'rcfz_co_fnd_be', 'rcfz_co_fnd_fs', 'rcfz_co_fnd_toi',
                 'rcfz_co_fnd_ft')
    def get_rcfz_co_fnd(self):
        for rec in self:
            rec.rcfz_co_fnd = (rec.rcfz_co_fnd_grip + rec.rcfz_co_fnd_sp +
                               rec.rcfz_co_fnd_bp + rec.rcfz_co_fnd_be +
                               rec.rcfz_co_fnd_fs + rec.rcfz_co_fnd_toi +
                               rec.rcfz_co_fnd_ft) / 7

    # RCFZ CO FRCS

    rcfz_co_frcs = fields.Float(
        string="CO: Forehand reverse cut straight",
        compute="get_rcfz_co_frcs", default=0,
        store=True)

    rcfz_co_frcs_grip = fields.Integer(
        string="Grip", default=0)
    rcfz_co_frcs_sp = fields.Integer(
        string="Starting Position", default=0)
    rcfz_co_frcs_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcfz_co_frcs_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcfz_co_frcs_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcfz_co_frcs_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcfz_co_frcs_ft = fields.Integer(
        string="Follow Through", default=0)

    rcfz_co_frcs_video = fields.Binary(
        string="CO: Forehand reverse cut straight video")

    @api.depends('rcfz_co_frcs_grip', 'rcfz_co_frcs_sp', 'rcfz_co_frcs_bp',
                 'rcfz_co_frcs_be', 'rcfz_co_frcs_fs', 'rcfz_co_frcs_toi',
                 'rcfz_co_frcs_ft')
    def get_rcfz_co_frcs(self):
        for rec in self:
            rec.rcfz_co_frcs = (rec.rcfz_co_frcs_grip + rec.rcfz_co_frcs_sp +
                                rec.rcfz_co_frcs_bp + rec.rcfz_co_frcs_be +
                                rec.rcfz_co_frcs_fs + rec.rcfz_co_frcs_toi +
                                rec.rcfz_co_frcs_ft) / 7

    # RCFZ CO DC

    rcfz_co_dc = fields.Float(
        string="CO to 50/50: Defensive clears",
        compute="get_rcfz_co_dc",
        default=0, store=True)

    rcfz_co_dc_grip = fields.Integer(
        string="Grip", default=0)
    rcfz_co_dc_sp = fields.Integer(
        string="Starting Position", default=0)
    rcfz_co_dc_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcfz_co_dc_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcfz_co_dc_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcfz_co_dc_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcfz_co_dc_ft = fields.Integer(
        string="Follow Through", default=0)

    rcfz_co_dc_video = fields.Binary(
        string="CO to 50/50: Defensive clears video")

    @api.depends('rcfz_co_dc_grip', 'rcfz_co_dc_sp', 'rcfz_co_dc_bp',
                 'rcfz_co_dc_be', 'rcfz_co_dc_fs', 'rcfz_co_dc_toi',
                 'rcfz_co_dc_ft')
    def get_rcfz_co_dc(self):
        for rec in self:
            rec.rcfz_co_dc = (rec.rcfz_co_dc_grip + rec.rcfz_co_dc_sp +
                                rec.rcfz_co_dc_bp + rec.rcfz_co_dc_be +
                                rec.rcfz_co_dc_fs + rec.rcfz_co_dc_toi +
                                rec.rcfz_co_dc_ft) / 7

    # RCFZ FN

    rcfz_fn = fields.Float(
        string="50/50: Forehand neutralisation",
        compute="get_rcfz_fn", default=0, store=True)

    rcfz_fn_grip = fields.Integer(
        string="Grip", default=0)
    rcfz_fn_sp = fields.Integer(
        string="Starting Position", default=0)
    rcfz_fn_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcfz_fn_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcfz_fn_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcfz_fn_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcfz_fn_ft = fields.Integer(
        string="Follow Through", default=0)

    rcfz_fn_video = fields.Binary(
        string="50/50: Forehand neutralisation video")

    @api.depends('rcfz_fn_grip', 'rcfz_fn_sp', 'rcfz_fn_bp',
                 'rcfz_fn_be', 'rcfz_fn_fs', 'rcfz_fn_toi',
                 'rcfz_fn_ft')
    def get_rcfz_fn(self):
        for rec in self:
            rec.rcfz_fn = (rec.rcfz_fn_grip + rec.rcfz_fn_sp +
                                rec.rcfz_fn_bp + rec.rcfz_fn_be +
                                rec.rcfz_fn_fs + rec.rcfz_fn_toi +
                                rec.rcfz_fn_ft) / 7

    # RCFZ TD FD

    rcfz_td_fd = fields.Float(string="TD: Forehand dive",
                              compute="get_rcfz_td_fd",
                              default=0, store=True)

    rcfz_td_fd_grip = fields.Integer(
        string="Grip", default=0)
    rcfz_td_fd_sp = fields.Integer(
        string="Starting Position", default=0)
    rcfz_td_fd_bp = fields.Integer(
        string="Backswing Position", default=0)
    rcfz_td_fd_be = fields.Integer(
        string="Backswing Endpoint", default=0)
    rcfz_td_fd_fs = fields.Integer(
        string="Forward Swing", default=0)
    rcfz_td_fd_toi = fields.Integer(
        string="Time of Impact", default=0)
    rcfz_td_fd_ft = fields.Integer(
        string="Follow Through", default=0)

    rcfz_td_fd_video = fields.Binary(string="TD: Forehand dive video")

    @api.depends('rcfz_td_fd_grip', 'rcfz_td_fd_sp', 'rcfz_td_fd_bp',
                 'rcfz_td_fd_be', 'rcfz_td_fd_fs', 'rcfz_td_fd_toi',
                 'rcfz_td_fd_ft')
    def get_rcfz_td_fd(self):
        for rec in self:
            rec.rcfz_td_fd = (rec.rcfz_td_fd_grip + rec.rcfz_td_fd_sp +
                                rec.rcfz_td_fd_bp + rec.rcfz_td_fd_be +
                                rec.rcfz_td_fd_fs + rec.rcfz_td_fd_toi +
                                rec.rcfz_td_fd_ft) / 7

    @api.depends('rcfz_to_js', 'rcfz_to_fbrs', 'rcfz_co_oc', 'rcfz_co_fcs',
                 'rcfz_co_fcc', 'rcfz_co_fnd', 'rcfz_co_frcs',
                 'rcfz_co_dc', 'rcfz_fn', 'rcfz_td_fd')
    def get_overall_rcfz(self):
        for assessment in self:
            assessment.overall_rcfz = (assessment.rcfz_to_js +
                                       assessment.rcfz_to_fbrs +
                                       assessment.rcfz_co_oc +
                                       assessment.rcfz_co_fcs +
                                       assessment.rcfz_co_fcc +
                                       assessment.rcfz_co_fnd +
                                       assessment.rcfz_co_frcs +
                                       assessment.rcfz_co_dc +
                                       assessment.rcfz_fn +
                                       assessment.rcfz_td_fd) / 10

    # Footwork Patterns

    overall_footwork = fields.Float(string="Overall footwork",
                                    compute="get_overall_footwork",
                                    default=0, store=True)

    #FOOTWORK OFP

    footwork_ofp = fields.Float(
        string="Offensive footwork pattern: 6 corners",
        compute="get_footwork_ofp", store=True, default=0)

    footwork_ofp_fnz = fields.Integer(string="FNZ", default=0)
    footwork_ofp_bnz = fields.Integer(string="BNZ", default=0)
    footwork_ofp_fmz = fields.Integer(string="FMZ", default=0)
    footwork_ofp_bmz = fields.Integer(string="BMZ", default=0)
    footwork_ofp_rcovhz = fields.Integer(string="RCOvhZ", default=0)
    footwork_ofp_rcfz = fields.Integer(string="RCFZ", default=0)

    footwork_ofp_video = fields.Binary(
        string="Offensive footwork pattern: 6 corners video")

    @api.depends('footwork_ofp_fnz', 'footwork_ofp_bnz', 'footwork_ofp_fmz',
                 'footwork_ofp_bmz', 'footwork_ofp_rcovhz', 'footwork_ofp_rcfz')
    def get_footwork_ofp(self):
        for rec in self:
            rec.footwork_ofp = (rec.footwork_ofp_fnz + rec.footwork_ofp_bnz +
                                rec.footwork_ofp_fmz + rec.footwork_ofp_bmz +
                                rec.footwork_ofp_rcovhz +
                                rec.footwork_ofp_rcfz) / 6

    footwork_dfp = fields.Float(
        string="Defensive footwork pattern: 6 corners",
        compute="get_footwork_dfp", default=0, store=True)

    footwork_dfp_fnz = fields.Integer(string="FNZ", default=0)
    footwork_dfp_bnz = fields.Integer(string="BNZ", default=0)
    footwork_dfp_fmz = fields.Integer(string="FMZ", default=0)
    footwork_dfp_bmz = fields.Integer(string="BMZ", default=0)
    footwork_dfp_rcbz = fields.Integer(string="RCBZ", default=0)
    footwork_dfp_rcfz = fields.Integer(string="RCFZ", default=0)

    footwork_dfp_video = fields.Binary(
        string="Defensive footwork pattern: 6 corners video")
    assessment_type_ids = fields.Many2many('assessment.types')
    current_rank = fields.Integer()

    @api.depends('footwork_dfp_fnz', 'footwork_dfp_bnz', 'footwork_dfp_fmz',
                 'footwork_dfp_bmz', 'footwork_dfp_rcbz', 'footwork_dfp_rcfz')
    def get_footwork_dfp(self):
        for rec in self:
            rec.footwork_dfp = (rec.footwork_dfp_fnz + rec.footwork_dfp_bnz +
                                rec.footwork_dfp_fmz + rec.footwork_dfp_bmz +
                                rec.footwork_dfp_rcbz +
                                rec.footwork_dfp_rcfz) / 6

    @api.depends('footwork_ofp', 'footwork_dfp')
    def get_overall_footwork(self):
        for assessment in self:
            assessment.overall_footwork = (assessment.footwork_ofp +
                                           assessment.footwork_dfp) / 2

    def _default_stage_id(self):
        """Setting default stage"""
        rec = self.env['badminto.assessment.stage'].browse(
            self.env.ref('badminto.stage_assessment').id)
        return rec.id if rec else None

    @api.model
    def _read_group_stage_ids(self, categories, domain, order):
        """ Read all the stages and display it in the kanban view,
            even if it is empty."""
        category_ids = categories._search([], order=order,
                                          access_rights_uid=SUPERUSER_ID)
        return categories.browse(category_ids)

    def upload_video_badminto(self, rec_id, file, name, fieldname):
        attachments_present = self.env['ir.attachment'].search([
            ('res_model', '=', 'badminto.assessment'),
            ('res_id', '=', rec_id),
            ('badminto_field_name', '=', fieldname)
        ]).unlink()
        attachment = self.env['ir.attachment'].create({
            'name': name,
            'badminto_video_file_data': file,
            'res_model': 'badminto.assessment',
            'res_id': rec_id,
            'badminto_field_name': fieldname,
        })

    def load_video_badminto(self, rec_id, fieldname):

        res = self.env['ir.attachment'].search(
            [('res_id', '=', rec_id),
             ('mimetype', '=', 'video/mp4'),
             ('res_model', '=', 'badminto.assessment'),
             ('badminto_field_name', '=', fieldname)])
        data = {}
        if res:
            data = {
                'name': res['name'],
                'datas': res['badminto_video_file_data']
            }
        return data

    def update_video_badminto(self, rec_id, fieldname):
        self.env['ir.attachment'].search([('res_id', '=', rec_id),
                                          ('res_model', '=',
                                           'badminto.assessment'),
                                          ('badminto_field_name', '=',
                                           fieldname)
                                          ]).unlink()

    def play_video_badminto(self, rec_id, fieldname):
        res = self.env['ir.attachment'].search([('res_id', '=', rec_id),
                                          ('res_model', '=',
                                           'badminto.assessment'),
                                          ('badminto_field_name', '=',
                                           fieldname)])
        data = {}
        if res:
            data = {
                'name': res['name'],
                'datas': res['badminto_video_file_data']
            }
        return data


class BadmintoAssessmentTags(models.Model):
    """ Tags of assessments """
    _name = "badminto.assessment.tags"
    _description = " Badminto Assessment Tags"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Name', required=True)
    color = fields.Integer(string='Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]


class BadmintoAssessmentStages(models.Model):
    """ Stages of assessments """
    _name = "badminto.assessment.stage"
    _description = "Badminto Assessment Stages"
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


class IrAttachmentInherit(models.Model):
    _inherit = 'ir.attachment'

    badminto_video_file_data = fields.Text()
    badminto_field_name = fields.Text()
