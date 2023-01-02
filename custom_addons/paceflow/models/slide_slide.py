from odoo import models, fields, api


class Slide(models.Model):
    _inherit = "slide.slide"

    is_drill = fields.Boolean(string="Is a drill", store=True, readonly=False,
                              compute='_compute_is_drill')
    legality = fields.Boolean(string="Legality drill", default=False,
                              store=True,)
    momentum = fields.Boolean(string="Momentum drill", default=False,
                              store=True,)
    stability = fields.Boolean(string="Stability drill", default=False,
                               store=True,)
    stability_rear = fields.Boolean(string="Stability rear view drill",
                                    default=False, store=True,)
    stability_side = fields.Boolean(string="Stability side view drill",
                                    default=False, store=True,)
    paceflow = fields.Boolean(string="Paceflow drill", default=False,
                              store=True,)
    paceflow_rear = fields.Boolean(string="Paceflow rear view drill",
                                   default=False, store=True,)
    paceflow_side = fields.Boolean(string="Paceflow side view drill",
                                   default=False, store=True,)
    order_sequence = fields.Integer()

    @api.depends('channel_id.is_paceflow_course')
    def _compute_is_drill(self):
        for rec in self:
            if rec.channel_id.is_paceflow_course:
                rec.is_drill = True
            else:
                rec.is_drill = False


class Channel(models.Model):
    _inherit = "slide.channel"

    is_paceflow_course = fields.Boolean(string="Is a pace-flow course",
                                        store=True, default=False)

    @api.onchange('is_paceflow_course')
    def _onchange_is_paceflow_course(self):
        course_partners = self.partner_ids
        self.env.cr.execute(
            """SELECT id from res_partner
               WHERE is_client = True""")
        client_ids = [client_id['id'] for client_id in self._cr.dictfetchall()]
        client_partners = self.env['res.partner'].browse(client_ids)
        if self.is_paceflow_course:
            for client_partner in client_partners:
                for course_partner in course_partners:
                    if client_partner == course_partner:
                        break
                    else:
                        self.env['slide.channel.partner'].create({
                            'channel_id': self._origin.id,
                            'partner_id': client_partner.id, })
                    break
        else:
            for client_partner in client_partners:
                for course_partner in course_partners:
                    if client_partner == course_partner:
                        self.env['slide.channel.partner'].search([
                            ('channel_id', '=', self._origin.id),
                            ('partner_id', '=', client_partner.id)]).unlink()
