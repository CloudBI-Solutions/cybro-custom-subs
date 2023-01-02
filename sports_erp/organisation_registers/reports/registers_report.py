from odoo import models, api


class VehicleReport(models.AbstractModel):
    _name = 'report.organisation_registers.report_organisation_registers'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("report values", docids, data)
        docs = self.env['athlete.groups'].browse(docids)
        print(docs.mapped('id'), "docs")
        registers = self.env['organisation.registers'].search([('group_id', 'in', docs.ids)])
        print(registers, "ggggg")
        return {
            'doc_ids': docids,
            'registers': registers,
            # 'doc_model': model.model,
            'docs': docs,
            'data': data,
        }