from odoo import api, fields, models, _


class ComponentTypeInherit(models.Model):
    _inherit = "component.type"

    component_type = fields.Selection([('cpu', 'CPU'),('board', 'Motherboard'),('cooler','Cooler'),('case','Case'),('memory','Memory'),('fans','Fans'),('gpu','GPU'),('power','Powersupply'),('m_2','M2'),('other','Other')], string="Type", default='other')


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    component_type = fields.Selection(related='component_id.component_type',
                                       store=True,string="Component Type")
    cooler_fans_count = fields.Integer('No. of fans')
    m_2_support = fields.Integer('Number of m.2 Support')

    m_2_no = fields.Integer('No of M2.')