from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    parent_name = fields.Char("Parent Name")
    parent_email = fields.Char("Parent Email")
    parent_phone = fields.Char("Parent Phone")
    dob = fields.Date("Date of Birth")
    emergency_contact_number_1 = fields.Char("Emergency Contact Number 1")
    emergency_contact_number_2 = fields.Char("Emergency Contact Number 2")
    signature = fields.Binary("Signature")
    medical_info = fields.Text('Medical Information')
    event_extension = fields.Boolean(related='event_id.event_extension')
