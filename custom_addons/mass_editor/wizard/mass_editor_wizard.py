from odoo import models, fields
from odoo.exceptions import ValidationError


class MassEditorWizard(models.TransientModel):
    _name = 'mass.editor.wizard'
    _description = 'Mass Editor Wizard'

    def model_set(self):
        """This is the function that sets
           the current model"""
        model = self.env['ir.model'].search([
            ('model', '=', self.env.context['active_model'])])
        return model.id

    model_id = fields.Many2one('ir.model', string='Model',
                               default=model_set, readonly=True)

    field_ids = fields.Many2many('ir.model.fields',
                                 required=True,
                                 select=True,
                                 domain="[('model_id', '=', model_id),"
                                        "('ttype', '!=', 'one2many'),"
                                        "('name', '!=', 'id')]")

    def btn_edit(self):
        """Function that is called when button
           is clicked. Passes the context
           model, selected fields and selected records"""
        if not self.field_ids:
            raise ValidationError("Choose the fields to edit !!!!")
        context = {
            'model': self.env.context['active_model'],
            'selected_records': self.env.context['selected_records'],
            'selected_fields': self.field_ids.ids
        }
        res = {
            'name': "Edit Window",
            'type': 'ir.actions.act_window',
            'res_model': 'edit.window.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': context,
        }
        return res
