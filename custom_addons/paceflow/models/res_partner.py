from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    last_name = fields.Char(string='Last Name')
    assessment_ids = fields.Many2many('assessment.assessment',
                                      string='Assessments')
    is_client = fields.Boolean(string="Coach", default=False)
    is_child = fields.Boolean(string="Player", default=False)
    hand = fields.Selection([('left', 'Left Handed'), ('right', 'Right Handed')
                             ], string="Hand")
    dob = fields.Date(string="DOB", )

    def view_assessments(self):
        assessments = self.env['assessment.assessment'].search(
            [('partner_id', '=', self.id)])
        return{
            'name': "Assessments",
            'type': 'ir.actions.act_window',
            'res_model': 'assessment.assessment',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', assessments.ids)]
        }
