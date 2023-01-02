# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Events(models.Model):
    _inherit = "organisation.coaches"

    booking_type_ids = fields.One2many('booking.type', 'coach_id',
                                       string="Appointment Types")
    sun = fields.Boolean(string="Sunday", default=True)
    mon = fields.Boolean(string="Monday", default=True)
    tue = fields.Boolean(string="Tuesday", default=True)
    wed = fields.Boolean(string="Wednesday", default=True)
    thu = fields.Boolean(string="Thursday", default=True)
    fri = fields.Boolean(string="Friday", default=True)
    sat = fields.Boolean(string="Saturday", default=True)
    mon_slot_ids = fields.One2many('slot.monday', 'coach_id', string="Monday")
    tue_slot_ids = fields.One2many('slot.tuesday', 'coach_id', string="Tuesday")
    wed_slot_ids = fields.One2many('slot.wednesday', 'coach_id',
                                   string="Wednesday")
    thu_slot_ids = fields.One2many('slot.thursday', 'coach_id',
                                   string="Thursday")
    fri_slot_ids = fields.One2many('slot.friday', 'coach_id', string="Friday")
    sat_slot_ids = fields.One2many('slot.saturday', 'coach_id',
                                   string="Saturday")
    sun_slot_ids = fields.One2many('slot.sunday', 'coach_id', string="Sunday")
    sun_from = fields.Float(string="From")
    sun_to = fields.Float(string="To")
    mon_from = fields.Float(string="From")
    mon_to = fields.Float(string="To")
    tue_from = fields.Float(string="From")
    tue_to = fields.Float(string="To")
    wed_from = fields.Float(string="From")
    wed_to = fields.Float(string="To")
    thu_from = fields.Float(string="From")
    thu_to = fields.Float(string="To")
    fri_from = fields.Float(string="From")
    fri_to = fields.Float(string="To")
    sat_from = fields.Float(string="From")
    sat_to = fields.Float(string="To")


class SlotMonday(models.Model):
    """model for managing slots for monday"""
    _name = "slot.monday"
    _description = "Slot Monday"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Ref")
    mon_from = fields.Float(string="From")
    mon_to = fields.Float(string="To")
    description = fields.Text(string="Description")
    coach_id = fields.Many2one('organisation.coaches', string="Coach")


class SlotTuesday(models.Model):
    """model for managing slots for tuesday"""
    _name = "slot.tuesday"
    _description = "Slot Tuesday"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Ref")
    tue_from = fields.Float(string="From")
    tue_to = fields.Float(string="To")
    description = fields.Text(string="Description")
    coach_id = fields.Many2one('organisation.coaches', string="Coach")


class SlotWednesday(models.Model):
    """model for managing slots for wednesday"""
    _name = "slot.wednesday"
    _description = "Slot Wednesday"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Ref")
    wed_from = fields.Float(string="From")
    wed_to = fields.Float(string="To")
    description = fields.Text(string="Description")
    coach_id = fields.Many2one('organisation.coaches', string="Coach")


class SlotThursday(models.Model):
    """model for managing slots for thursday"""
    _name = "slot.thursday"
    _description = "Slot Thursday"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Ref")
    thu_from = fields.Float(string="From")
    thu_to = fields.Float(string="To")
    description = fields.Text(string="Description")
    coach_id = fields.Many2one('organisation.coaches', string="Coach")


class SlotFriday(models.Model):
    """model for managing slots for friday"""
    _name = "slot.friday"
    _description = "Slot Friday"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Ref")
    fri_from = fields.Float(string="From")
    fri_to = fields.Float(string="To")
    description = fields.Text(string="Description")
    coach_id = fields.Many2one('organisation.coaches', string="Coach")


class SlotSaturday(models.Model):
    """model for managing slots for saturday"""
    _name = "slot.saturday"
    _description = "Slot Saturday"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Ref")
    sat_from = fields.Float(string="From")
    sat_to = fields.Float(string="To")
    description = fields.Text(string="Description")
    coach_id = fields.Many2one('organisation.coaches', string="Coach")


class SlotSunday(models.Model):
    """model for managing slots for sunday"""
    _name = "slot.sunday"
    _description = "Slot Sunday"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Ref")
    sun_from = fields.Float(string="From")
    sun_to = fields.Float(string="To")
    description = fields.Text(string="Description")
    coach_id = fields.Many2one('organisation.coaches', string="Coach")
