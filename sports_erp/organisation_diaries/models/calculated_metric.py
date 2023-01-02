from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError, UserError


class CalculatedMetric(models.Model):
    _name = 'calculated.metric'

    name = fields.Char(required=True)
    operator = fields.Many2one('calculated.metric.operator')
    number = fields.Integer()
    formula = fields.Char()
    operand_1 = fields.Many2one('calculated.metric')
    operand_2 = fields.Many2one('calculated.metric')
    organisation_id = fields.Many2one('organisation.organisation')
    visualization_configuration_ids = fields.One2many(
        'assessment.visualization.configuration', 'metric_id')
    formula = fields.Text(string='Formula for box qty for SO',
                                     default='''
                            # Available variables:
                            #----------------------
                            # order_qty: object containing the ordered quanity
                            # qty_per_box: object containing box per quantity
                            # order_qty_1 - order_qty_2: objects conating the order_qty_1 to order_qty_10

                            # Note: returned value have to be set in the variable 'result'

                            ''')

    _sql_constraints = [('name', 'UNIQUE (name)',
                         'You can not have two metric with the same Name !')]


class AssessmentVisualConfiguration(models.Model):
    _name = 'assessment.visualization.configuration'

    start = fields.Integer()
    end = fields.Integer()
    metric_id = fields.Many2one('calculated.metric')
    question_id = fields.Many2one('survey.question')
    color = fields.Selection([('red', 'Red'), ('yellow', 'Yellow'),
                              ('green', 'Green')], readonly=True)
    level = fields.Selection([('low', 'Low'), ('medium', 'Medium'),
                              ('high', 'High')])
    comments = fields.Text()

    @api.onchange('level')
    def onchange_level(self):
        if self.level == 'low':
            self.color = 'red'
        elif self.level == 'medium':
            self.color = 'yellow'
        elif self.level == 'high':
            self.color = 'green'

    def create(self, vals):
        for val in vals:
            print(val, )
            visual_records = self.env['assessment.visualization.configuration'].search(
                [('question_id', '=', val.get('question_id'))])
            records = self.env['assessment.visualization.configuration'].search(
                [('question_id', '=', val.get('question_id')),
                 ('level', '=', val.get('level'))])
            if records:
                raise UserError(
                    _("Can not create a configuration with same level twice"))
            if len(visual_records) == 3:
                raise UserError(
                    _("Can not create a new visualisation configuration"))
        print(records, "records")
        res = super(AssessmentVisualConfiguration, self).create(vals)
        return res


class CalculatedMetricOperator(models.Model):
    _name = 'calculated.metric.operator'
    _sql_constraints = [
        ('type_unique', 'unique (type)',
         "A Operator of this type already exists."),
    ]

    name = fields.Char('Name', required=1)
    type = fields.Selection([('add', 'Addition'), ('subtract', 'Subtraction'),
                             ('multiply', 'Multiplication'),
                             ('divide', 'Division')],
                            string='Type', default='add')