from odoo import models, fields, api


class Attendee(models.Model):
    _inherit = "calendar.attendee"

    def _send_mail_to_attendees(self, template_xmlid, force_send=False,
                                ignore_recurrence=False):
        if self.env.context.get('active_model') == "project.project":
            return
        else:
            res = super(Attendee, self)._send_mail_to_attendees(template_xmlid,
                                                                force_send=False,
                                                                ignore_recurrence=False)
            return res
