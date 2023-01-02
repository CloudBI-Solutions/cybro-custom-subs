from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KsDashboardNinjaBoard(models.Model):
    _inherit = 'ks_dashboard_ninja.board'

    show_in_portal = fields.Boolean(string="Show in portal", copy=False)

    @api.constrains('show_in_portal')
    def _check_show_in_portal_constraint(self):
        for rec in self.filtered(lambda p: p.show_in_portal):
            domain = [('id', '!=', rec.id), ('show_in_portal', '=',True)]
            if self.search(domain):
                raise ValidationError(_('Show in portal must be unique!'))