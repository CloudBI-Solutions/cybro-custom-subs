
import json
from odoo import fields, _
import logging
from odoo import http
from odoo.http import request, route
from odoo.addons.survey.controllers.main import Survey
import werkzeug
from datetime import datetime
import pytz
from datetime import timedelta
from odoo.addons.website.controllers import form


class TechnicalAssessmentController(http.Controller):

    @route(['/my/technical/assessment/sr'],
           type='http', auth='user', website=True)
    def technical_sr(self, **kw):
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(kw.get('assessment')))

        organisation_id = request.env[
            'organisation.organisation'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)])

        in_service_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.in_service_technical'))
        in_receive_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.in_receiving_technical'))

        if assessment.service_grip and assessment.service_sp and \
                assessment.service_bp and assessment.service_be and \
                assessment.service_fs and assessment.service_toi and \
                assessment.service_ft:
            service_complete = True
        else:
            service_complete = False
        if assessment.receiving_grip and assessment.receiving_sp and \
                assessment.receiving_bp and assessment.receiving_be and \
                assessment.receiving_fs and assessment.receiving_toi and \
                assessment.receiving_ft:
            receiving_complete = True
        else:
            receiving_complete = False
        values = {
            'is_account': True,
            'assessment': assessment,
            'organisation': organisation_id,
            'service_complete': service_complete,
            'receiving_complete': receiving_complete,
            'in_service': in_service_values,
            'in_receiving': in_receive_values,
        }
        return request.render('badminto.technical_sr_template', values)

    @route(['/my/technical/assessment/fnz'],
           type='http', auth='user', website=True)
    def technical_fnz(self, **kw):
        print('kwww', kw)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(kw.get('assessment')))

        organisation_id = request.env[
            'organisation.organisation'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)])

        fnz_to_fnk_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_to_forehand_technical'))

        fnz_co_fnp_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_co_forehand_technical'))

        fnz_co_ofcn_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_co_offensive_technical'))

        fnz_co_fol_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_co_forehand_offensive_lift_technical'))

        fnz_co_fss_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_co_forehand_straight_spin_technical'))

        fnz_co_frs_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_co_forehand_reverse_spin_technical'))

        fnz_co_nb_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_co_net_block_technical'))

        fnz_frs_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_forehand_reverse_spin_technical'))

        fnz_neutralisation_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_neutralisation_technical'))

        fnz_cd_dfcn_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_defensive_forehand_cross_net_technical'))

        fnz_cd_dfl_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_defensive_forehand_lifts_technical'))

        fnz_td_dd_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fnz_defensive_dive_technical'))

        if assessment.fnz_to_fnk_grip and assessment.fnz_to_fnk_sp and \
                assessment.fnz_to_fnk_bp and assessment.fnz_to_fnk_be and \
                assessment.fnz_to_fnk_fs and assessment.fnz_to_fnk_toi and \
                assessment.fnz_to_fnk_ft:
            fnz_to_fnk_complete = True
        else:
            fnz_to_fnk_complete = False

        if assessment.fnz_co_fnp_grip and assessment.fnz_co_fnp_sp and \
                assessment.fnz_co_fnp_bp and assessment.fnz_co_fnp_be and \
                assessment.fnz_co_fnp_fs and assessment.fnz_co_fnp_toi and \
                assessment.fnz_co_fnp_ft:
            fnz_co_fnp_complete = True
        else:
            fnz_co_fnp_complete = False

        if assessment.fnz_co_ofcn_grip and assessment.fnz_co_ofcn_sp and \
                assessment.fnz_co_ofcn_bp and assessment.fnz_co_ofcn_be and \
                assessment.fnz_co_ofcn_fs and assessment.fnz_co_ofcn_toi and \
                assessment.fnz_co_ofcn_ft:
            fnz_co_ofcn_complete = True
        else:
            fnz_co_ofcn_complete = False

        if assessment.fnz_co_fol_grip and assessment.fnz_co_fol_sp and \
                assessment.fnz_co_fol_bp and assessment.fnz_co_fol_be and \
                assessment.fnz_co_fol_fs and assessment.fnz_co_fol_toi and \
                assessment.fnz_co_fol_ft:
            fnz_co_fol_complete = True
        else:
            fnz_co_fol_complete = False

        if assessment.fnz_co_fss_grip and assessment.fnz_co_fss_sp and \
                assessment.fnz_co_fss_bp and assessment.fnz_co_fss_be and \
                assessment.fnz_co_fss_fs and assessment.fnz_co_fss_toi and \
                assessment.fnz_co_fss_ft:
            fnz_co_fss_complete = True
        else:
            fnz_co_fss_complete = False

        if assessment.fnz_co_frs_grip and assessment.fnz_co_frs_sp and \
                assessment.fnz_co_frs_bp and assessment.fnz_co_frs_be and \
                assessment.fnz_co_frs_fs and assessment.fnz_co_frs_toi and \
                assessment.fnz_co_frs_ft:
            fnz_co_frs_complete = True
        else:
            fnz_co_frs_complete = False

        if assessment.fnz_co_nb_grip and assessment.fnz_co_nb_sp and \
                assessment.fnz_co_nb_bp and assessment.fnz_co_nb_be and \
                assessment.fnz_co_nb_fs and assessment.fnz_co_nb_toi and \
                assessment.fnz_co_nb_ft:
            fnz_co_nb_complete = True
        else:
            fnz_co_nb_complete = False

        if assessment.fnz_frs_grip and assessment.fnz_frs_sp and \
                assessment.fnz_frs_bp and assessment.fnz_frs_be and \
                assessment.fnz_frs_fs and assessment.fnz_frs_toi and \
                assessment.fnz_frs_ft:
            fnz_frs_complete = True
        else:
            fnz_frs_complete = False

        if assessment.fnz_neutralisation_grip and assessment.fnz_neutralisation_sp and \
                assessment.fnz_neutralisation_bp and assessment.fnz_neutralisation_be and \
                assessment.fnz_neutralisation_fs and assessment.fnz_neutralisation_toi and \
                assessment.fnz_neutralisation_ft:
            fnz_neutralisation_complete = True
        else:
            fnz_neutralisation_complete = False

        if assessment.fnz_cd_dfcn_grip and assessment.fnz_cd_dfcn_sp and \
                assessment.fnz_cd_dfcn_bp and assessment.fnz_cd_dfcn_be and \
                assessment.fnz_cd_dfcn_fs and assessment.fnz_cd_dfcn_toi and \
                assessment.fnz_cd_dfcn_ft:
            fnz_cd_dfcn_complete = True
        else:
            fnz_cd_dfcn_complete = False

        if assessment.fnz_cd_dfl_grip and assessment.fnz_cd_dfl_sp and \
                assessment.fnz_cd_dfl_bp and assessment.fnz_cd_dfl_be and \
                assessment.fnz_cd_dfl_fs and assessment.fnz_cd_dfl_toi and \
                assessment.fnz_cd_dfl_ft:
            fnz_cd_dfl_complete = True
        else:
            fnz_cd_dfl_complete = False

        if assessment.fnz_td_dd_grip and assessment.fnz_td_dd_sp and \
                assessment.fnz_td_dd_bp and assessment.fnz_td_dd_be and \
                assessment.fnz_td_dd_fs and assessment.fnz_td_dd_toi and \
                assessment.fnz_td_dd_ft:
            fnz_td_dd_complete = True
        else:
            fnz_td_dd_complete = False

        values = {
            'is_account': True,
            'assessment': assessment,
            'organisation': organisation_id,
            'fnz_to_fnk_complete': fnz_to_fnk_complete,
            'fnz_co_fnp_complete': fnz_co_fnp_complete,
            'fnz_co_ofcn_complete': fnz_co_ofcn_complete,
            'fnz_co_fol_complete': fnz_co_fol_complete,
            'fnz_co_fss_complete': fnz_co_fss_complete,
            'fnz_co_frs_complete': fnz_co_frs_complete,
            'fnz_co_nb_complete': fnz_co_nb_complete,
            'fnz_frs_complete': fnz_frs_complete,
            'fnz_neutralisation_complete': fnz_neutralisation_complete,
            'fnz_cd_dfcn_complete': fnz_cd_dfcn_complete,
            'fnz_cd_dfl_complete': fnz_cd_dfl_complete,
            'fnz_td_dd_complete': fnz_td_dd_complete,
            'fnz_to_fnk': fnz_to_fnk_values,
            'fnz_co_fnp': fnz_co_fnp_values,
            'fnz_co_ofcn': fnz_co_ofcn_values,
            'fnz_co_fol': fnz_co_fol_values,
            'fnz_co_fss': fnz_co_fss_values,
            'fnz_co_frs': fnz_co_frs_values,
            'fnz_co_nb': fnz_co_nb_values,
            'fnz_frs': fnz_frs_values,
            'fnz_neutralisation': fnz_neutralisation_values,
            'fnz_cd_dfcn': fnz_cd_dfcn_values,
            'fnz_cd_dfl': fnz_cd_dfl_values,
            'fnz_td_dd': fnz_td_dd_values,
        }
        return request.render('badminto.technical_fnz_template', values)

    @route(['/my/technical/assessment/bnz'],
           type='http', auth='user', website=True)
    def technical_bnz(self, **kw):
        print('kwww', kw)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(kw.get('assessment')))

        organisation_id = request.env[
            'organisation.organisation'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)])

        bnz_to_fnk_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_to_fnk_technical'))

        bnz_co_fnp_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_co_fnp_technical'))

        bnz_co_ofcn_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_co_ofcn_technical'))

        bnz_co_fol_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_co_fol_technical'))

        bnz_co_fss_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_co_fss_technical'))

        bnz_co_frs_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_co_frs_technical'))

        bnz_co_nb_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_co_nb_technical'))

        bnz_frs_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_frs_technical'))

        bnz_neutralisation_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_neutralisation_technical'))

        bnz_cd_dfcn_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_cd_dfcn_technical'))

        bnz_cd_dfl_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_cd_dfl_technical'))

        bnz_td_dd_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.bnz_td_dd_technical'))

        if assessment.bnz_to_fnk_grip and assessment.bnz_to_fnk_sp and \
                assessment.bnz_to_fnk_bp and assessment.bnz_to_fnk_be and \
                assessment.bnz_to_fnk_fs and assessment.bnz_to_fnk_toi and \
                assessment.bnz_to_fnk_ft:
            bnz_to_fnk_complete = True
        else:
            bnz_to_fnk_complete = False

        if assessment.bnz_co_fnp_grip and assessment.bnz_co_fnp_sp and \
                assessment.bnz_co_fnp_bp and assessment.bnz_co_fnp_be and \
                assessment.bnz_co_fnp_fs and assessment.bnz_co_fnp_toi and \
                assessment.bnz_co_fnp_ft:
            bnz_co_fnp_complete = True
        else:
            bnz_co_fnp_complete = False

        if assessment.bnz_co_ofcn_grip and assessment.bnz_co_ofcn_sp and \
                assessment.bnz_co_ofcn_bp and assessment.bnz_co_ofcn_be and \
                assessment.bnz_co_ofcn_fs and assessment.bnz_co_ofcn_toi and \
                assessment.bnz_co_ofcn_ft:
            bnz_co_ofcn_complete = True
        else:
            bnz_co_ofcn_complete = False

        if assessment.bnz_co_fol_grip and assessment.bnz_co_fol_sp and \
                assessment.bnz_co_fol_bp and assessment.bnz_co_fol_be and \
                assessment.bnz_co_fol_fs and assessment.bnz_co_fol_toi and \
                assessment.bnz_co_fol_ft:
            bnz_co_fol_complete = True
        else:
            bnz_co_fol_complete = False

        if assessment.bnz_co_fss_grip and assessment.bnz_co_fss_sp and \
                assessment.bnz_co_fss_bp and assessment.bnz_co_fss_be and \
                assessment.bnz_co_fss_fs and assessment.bnz_co_fss_toi and \
                assessment.bnz_co_fss_ft:
            bnz_co_fss_complete = True
        else:
            bnz_co_fss_complete = False

        if assessment.bnz_co_frs_grip and assessment.bnz_co_frs_sp and \
                assessment.bnz_co_frs_bp and assessment.bnz_co_frs_be and \
                assessment.bnz_co_frs_fs and assessment.bnz_co_frs_toi and \
                assessment.bnz_co_frs_ft:
            bnz_co_frs_complete = True
        else:
            bnz_co_frs_complete = False

        if assessment.bnz_co_nb_grip and assessment.bnz_co_nb_sp and \
                assessment.bnz_co_nb_bp and assessment.bnz_co_nb_be and \
                assessment.bnz_co_nb_fs and assessment.bnz_co_nb_toi and \
                assessment.bnz_co_nb_ft:
            bnz_co_nb_complete = True
        else:
            bnz_co_nb_complete = False

        if assessment.bnz_frs_grip and assessment.bnz_frs_sp and \
                assessment.bnz_frs_bp and assessment.bnz_frs_be and \
                assessment.bnz_frs_fs and assessment.bnz_frs_toi and \
                assessment.bnz_frs_ft:
            bnz_frs_complete = True
        else:
            bnz_frs_complete = False

        if assessment.bnz_neutralisation_grip and assessment.bnz_neutralisation_sp and \
                assessment.bnz_neutralisation_bp and assessment.bnz_neutralisation_be and \
                assessment.bnz_neutralisation_fs and assessment.bnz_neutralisation_toi and \
                assessment.bnz_neutralisation_ft:
            bnz_neutralisation_complete = True
        else:
            bnz_neutralisation_complete = False

        if assessment.bnz_cd_dfcn_grip and assessment.bnz_cd_dfcn_sp and \
                assessment.bnz_cd_dfcn_bp and assessment.bnz_cd_dfcn_be and \
                assessment.bnz_cd_dfcn_fs and assessment.bnz_cd_dfcn_toi and \
                assessment.bnz_cd_dfcn_ft:
            bnz_cd_dfcn_complete = True
        else:
            bnz_cd_dfcn_complete = False

        if assessment.bnz_cd_dfl_grip and assessment.bnz_cd_dfl_sp and \
                assessment.bnz_cd_dfl_bp and assessment.bnz_cd_dfl_be and \
                assessment.bnz_cd_dfl_fs and assessment.bnz_cd_dfl_toi and \
                assessment.bnz_cd_dfl_ft:
            bnz_cd_dfl_complete = True
        else:
            bnz_cd_dfl_complete = False

        if assessment.bnz_td_dd_grip and assessment.bnz_td_dd_sp and \
                assessment.bnz_td_dd_bp and assessment.bnz_td_dd_be and \
                assessment.bnz_td_dd_fs and assessment.bnz_td_dd_toi and \
                assessment.bnz_td_dd_ft:
            bnz_td_dd_complete = True
        else:
            bnz_td_dd_complete = False

        values = {
            'is_account': True,
            'assessment': assessment,
            'organisation': organisation_id,
            'bnz_to_fnk_complete': bnz_to_fnk_complete,
            'bnz_co_fnp_complete': bnz_co_fnp_complete,
            'bnz_co_ofcn_complete': bnz_co_ofcn_complete,
            'bnz_co_fol_complete': bnz_co_fol_complete,
            'bnz_co_fss_complete': bnz_co_fss_complete,
            'bnz_co_frs_complete': bnz_co_frs_complete,
            'bnz_co_nb_complete': bnz_co_nb_complete,
            'bnz_frs_complete': bnz_frs_complete,
            'bnz_neutralisation_complete': bnz_neutralisation_complete,
            'bnz_cd_dfcn_complete': bnz_cd_dfcn_complete,
            'bnz_cd_dfl_complete': bnz_cd_dfl_complete,
            'bnz_td_dd_complete': bnz_td_dd_complete,
            'bnz_to_fnk': bnz_to_fnk_values,
            'bnz_co_fnp': bnz_co_fnp_values,
            'bnz_co_ofcn': bnz_co_ofcn_values,
            'bnz_co_fol': bnz_co_fol_values,
            'bnz_co_fss': bnz_co_fss_values,
            'bnz_co_frs': bnz_co_frs_values,
            'bnz_co_nb': bnz_co_nb_values,
            'bnz_frs': bnz_frs_values,
            'bnz_neutralisation': bnz_neutralisation_values,
            'bnz_cd_dfcn': bnz_cd_dfcn_values,
            'bnz_cd_dfl': bnz_cd_dfl_values,
            'bnz_td_dd': bnz_td_dd_values,
        }
        return request.render('badminto.technical_bnz_template', values)

    @route(['/my/technical/assessment/fmz'],
           type='http', auth='user', website=True)
    def technical_fmz(self, **kw):
        print('kwww', kw)
        assessment = request.env['badminto.assessment'].sudo().browse(
            int(kw.get('assessment')))

        organisation_id = request.env[
            'organisation.organisation'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)])

        fmz_co_ss_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fmz_co_ss_technical'))

        fmz_fmcp_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fmz_fmcp_technical'))

        fmz_cd_fds_s_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fmz_cd_fds_s_technical'))

        fmz_cd_fdc_s_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fmz_cd_fdc_s_technical'))

        fmz_cd_fds_l_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fmz_cd_fds_l_technical'))

        fmz_cd_fdc_l_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fmz_cd_fdc_l_technical'))

        fmz_cd_fdca_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fmz_cd_fdca_technical'))

        fmz_fd_values = organisation_id.technical_configuration_ids.filtered(
            lambda x: x.type == request.env.ref(
                'badminto.fmz_fd_technical'))

        if assessment.fmz_co_ss_grip and assessment.fmz_co_ss_sp and \
                assessment.fmz_co_ss_bp and assessment.fmz_co_ss_be and \
                assessment.fmz_co_ss_fs and assessment.fmz_co_ss_toi and \
                assessment.fmz_co_ss_ft:
            fmz_co_ss_complete = True
        else:
            fmz_co_ss_complete = False

        if assessment.fmz_fmcp_grip and assessment.fmz_fmcp_sp and \
                assessment.fmz_fmcp_bp and assessment.fmz_fmcp_be and \
                assessment.fmz_fmcp_fs and assessment.fmz_fmcp_toi and \
                assessment.fmz_fmcp_ft:
            fmz_fmcp_complete = True
        else:
            fmz_fmcp_complete = False

        if assessment.fmz_cd_fds_s_grip and assessment.fmz_cd_fds_s_sp and \
                assessment.fmz_cd_fds_s_bp and assessment.fmz_cd_fds_s_be and \
                assessment.fmz_cd_fds_s_fs and assessment.fmz_cd_fds_s_toi and \
                assessment.fmz_cd_fds_s_ft:
            fmz_cd_fds_s_complete = True
        else:
            fmz_cd_fds_s_complete = False

        if assessment.fmz_cd_fdc_s_grip and assessment.fmz_cd_fdc_s_sp and \
                assessment.fmz_cd_fdc_s_bp and assessment.fmz_cd_fdc_s_be and \
                assessment.fmz_cd_fdc_s_fs and assessment.fmz_cd_fdc_s_toi and \
                assessment.fmz_cd_fdc_s_ft:
            fmz_cd_fdc_s_complete = True
        else:
            fmz_cd_fdc_s_complete = False

        if assessment.fmz_cd_fds_l_grip and assessment.fmz_cd_fds_l_sp and \
                assessment.fmz_cd_fds_l_bp and assessment.fmz_cd_fds_l_be and \
                assessment.fmz_cd_fds_l_fs and assessment.fmz_cd_fds_l_toi and \
                assessment.fmz_cd_fds_l_ft:
            fmz_cd_fds_l_complete = True
        else:
            fmz_cd_fds_l_complete = False

        if assessment.fmz_cd_fdc_l_grip and assessment.fmz_cd_fdc_l_sp and \
                assessment.fmz_cd_fdc_l_bp and assessment.fmz_cd_fdc_l_be and \
                assessment.fmz_cd_fdc_l_fs and assessment.fmz_cd_fdc_l_toi and \
                assessment.fmz_cd_fdc_l_ft:
            fmz_cd_fdc_l_complete = True
        else:
            fmz_cd_fdc_l_complete = False

        if assessment.fmz_cd_fdca_grip and assessment.fmz_cd_fdca_sp and \
                assessment.fmz_cd_fdca_bp and assessment.fmz_cd_fdca_be and \
                assessment.fmz_cd_fdca_fs and assessment.fmz_cd_fdca_toi and \
                assessment.fmz_cd_fdca_ft:
            fmz_cd_fdca_complete = True
        else:
            fmz_cd_fdca_complete = False

        if assessment.fmz_fd_grip and assessment.fmz_fd_sp and \
                assessment.fmz_fd_bp and assessment.fmz_fd_be and \
                assessment.fmz_fd_fs and assessment.fmz_fd_toi and \
                assessment.fmz_fd_ft:
            fmz_fd_complete = True
        else:
            fmz_fd_complete = False

        values = {
            'is_account': True,
            'assessment': assessment,
            'organisation': organisation_id,
            'fmz_co_ss_complete': fmz_co_ss_complete,
            'fmz_fmcp_complete': fmz_fmcp_complete,
            'fmz_cd_fds_s_complete': fmz_cd_fds_s_complete,
            'fmz_cd_fdc_s_complete': fmz_cd_fdc_s_complete,
            'fmz_cd_fds_l_complete': fmz_cd_fds_l_complete,
            'fmz_cd_fdc_l_complete': fmz_cd_fdc_l_complete,
            'fmz_cd_fdca_complete': fmz_cd_fdca_complete,
            'fmz_fd_complete': fmz_fd_complete,
            'fmz_co_ss': fmz_co_ss_values,
            'fmz_fmcp': fmz_fmcp_values,
            'fmz_cd_fds_s': fmz_cd_fds_s_values,
            'fmz_cd_fdc_s': fmz_cd_fdc_s_values,
            'fmz_cd_fds_l': fmz_cd_fds_l_values,
            'fmz_cd_fdc_l': fmz_cd_fdc_l_values,
            'fmz_cd_fdca': fmz_cd_fdca_values,
            'fmz_fd': fmz_fd_values,
        }
        return request.render('badminto.technical_fmz_template', values)


