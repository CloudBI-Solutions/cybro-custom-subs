from odoo import fields, models


class Partner(models.Model):
    """inherited res partner"""
    _inherit = "res.partner"

    last_name = fields.Char(string='Last Name')
    organisation_ids = fields.Many2many('organisation.organisation',
                                        'partner_organisation_rel',
                                        'partner_id', 'org_id',
                                        string="Organisations")
    related_partner_id = fields.Integer(readonly=True)

    def name_get(self):
        result = []
        for rec in self:
            if rec.last_name:
                name = rec.name + ' ' + rec.last_name
                result.append((rec.id, name))
            else:
                name = rec.name
                result.append((rec.id, name))
        return result