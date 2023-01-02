from lxml import etree
from odoo import models, api


class EditWindowWizard(models.TransientModel):
    _name = 'edit.window.wizard'
    _description = 'Edit Window'

    @api.model
    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', toolbar=False):
        """This function sets the dynamic
           view of the wizard from where
           we can edit the fields"""
        model = self.env[self.env.context.get('model')]
        all_fields = model.fields_get()
        selected_fields = self.env['ir.model.fields'].browse(
            self.env.context.get('selected_fields'))
        form = etree.Element('form')
        div = etree.SubElement(form, 'div')
        etree.SubElement(div, 'label', {
            'string': '''Actions performed here will
                         affect all the selected records !!!''',
            'style': 'color:red;font-size:18px',
        })
        etree.SubElement(div, 'div')
        model_fields = {}

        for field in selected_fields:
            div_2 = etree.SubElement(form, 'div')
            group = etree.SubElement(div_2, 'group')

            if field.ttype == "many2one":
                etree.SubElement(group, 'field', {
                    'name': field.name,
                })
                model_fields[field.name] = {
                    'type': field.ttype,
                    'string': field.field_description,
                    'relation': field.relation,
                }

            elif field.ttype == "many2many":
                etree.SubElement(group, 'field', {
                    'name': field.name,
                })
                model_fields[field.name] = all_fields[field.name]

            elif field.ttype == 'selection':
                etree.SubElement(group, 'field', {
                    'name': field.name,
                })
                model_fields[field.name] = {
                    'type': field.ttype,
                    'string': field.field_description,
                    'selection': all_fields[field.name]['selection'],
                }
            else:
                etree.SubElement(group, 'field', {
                    'name': field.name,
                })
                model_fields[field.name] = {
                    'type': field.ttype,
                    'string': field.field_description,
                    }

        footer = etree.SubElement(div, 'footer')
        etree.SubElement(footer, 'button', {
            'name': 'action_apply_changes',
            'string': 'Apply Changes',
            'class': 'btn-primary',
            'type': 'object',
        })
        etree.SubElement(footer, 'button', {
            'string': 'Close',
            'class': 'btn-default',
            'special': 'cancel',
        })
        res = super(EditWindowWizard, self).fields_view_get()
        res['fields'] = model_fields
        root_tree = form.getroottree()
        res['arch'] = etree.tostring(root_tree)
        return res

    @api.model
    def create(self, vals):
        """Here, we create the records
           with updated vals"""
        model = self.env[self.env.context.get('model')]
        selected_records = model.browse(
            self.env.context.get('selected_records'))
        for rec in selected_records:
            rec.write(vals)
        return super(EditWindowWizard, self).create({})

    def read(self, fields=None, load='_classic_read'):
        """We update the fields that are in
           self._fields to a dictionary
           with false value and return it"""
        x_fields = {}
        for field in fields:
            if field in self._fields:
                x_fields.update({field: False})
        print(x_fields)
        return super(EditWindowWizard, self).read(x_fields, load=load)

    def action_apply_changes(self):
        """return the button action"""
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }
