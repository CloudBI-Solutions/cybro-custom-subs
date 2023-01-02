from odoo import fields, models


class CoachDashboardLink(models.Model):
    _name = "coach.dashboard.link"
    _description = "Coach Dashboard Link"
    _order = "sequence"

    name = fields.Char(string="Tile Name", required=True, copy=False)
    link = fields.Char(string="Tile Link", required=True, copy=False)
    tile_active = fields.Boolean(string='Active', default=True)
    dynamic_link = fields.Boolean(string='Dynamic Link', default=True)
    icon = fields.Binary("Icon")
    tile_background_color_1 = fields.Char(default="#fe5f75", help="Default background color of the dashboard tile",
                                          string="Tile Color #1")
    tile_background_color_2 = fields.Char(default="#fc9842", help="Default background color of the dashboard tile",
                                          string="Tile Color #2")
    tile_text_color = fields.Char(default="#000000", help="Default text color of the dashboard tile")

    # icon = fields.Binary("Icon", default='_get_default_image')
    sequence = fields.Integer(string='Sequence', default='_default_sequence')

    # @api.model
    # def _get_default_image(self):
    #     image_path = modules.get_module_resource('organisation_ui', 'static/src/img', 'icon.png')
    #     return base64.b64encode(open(image_path, 'rb').read())

    def _default_sequence(self):
        """Sort new records at the end of the list."""
        sequence = 0
        for record in self.search([]):
            sequence = max(sequence, record.sequence + 1)
            return sequence


class AthleteDashboardLink(models.Model):
    _name = "athlete.dashboard.link"
    _description = "Athlete Dashboard Link"
    _order = "sequence"

    name = fields.Char(string="Tile Name", required=True, copy=False)
    link = fields.Char(string="Tile Link", required=True, copy=False)
    tile_active = fields.Boolean(string='Active', default=True)
    dynamic_link = fields.Boolean(string='Dynamic Link', default=True)
    icon = fields.Binary("Icon")
    tile_background_color_1 = fields.Char(default="#fe5f75", help="Default background color of the dashboard tile",
                                          string="Tile Color #1")
    tile_background_color_2 = fields.Char(default="#fc9842", help="Default background color of the dashboard tile",
                                          string="Tile Color #2")
    tile_text_color = fields.Char(default="#000000", help="Default text color of the dashboard tile")
    sequence = fields.Integer(string='Sequence', default='_default_sequence')

    def _default_sequence(self):
        """Sort new records at the end of the list."""
        sequence = 0
        for record in self.search([]):
            sequence = max(sequence, record.sequence + 1)
            return sequence


class FanDashboardLink(models.Model):
    _name = "fan.dashboard.link"
    _description = "Fan Dashboard Link"
    _order = "sequence"

    name = fields.Char(string="Tile Name", required=True, copy=False)
    link = fields.Char(string="Tile Link", required=True, copy=False)
    tile_active = fields.Boolean(string='Active', default=True)
    dynamic_link = fields.Boolean(string='Dynamic Link', default=True)
    icon = fields.Binary("Icon")
    tile_background_color_1 = fields.Char(default="#fe5f75", help="Default background color of the dashboard tile",
                                          string="Tile Color #1")
    tile_background_color_2 = fields.Char(default="#fc9842", help="Default background color of the dashboard tile",
                                          string="Tile Color #2")
    tile_text_color = fields.Char(default="#000000", help="Default text color of the dashboard tile")
    sequence = fields.Integer(string='Sequence', default='_default_sequence')

    def _default_sequence(self):
        """Sort new records at the end of the list."""
        sequence = 0
        for record in self.search([]):
            sequence = max(sequence, record.sequence + 1)
            return sequence


class ParentDashboardLink(models.Model):
    _name = "parent.dashboard.link"
    _description = "Parent Dashboard Link"
    _order = "sequence"

    name = fields.Char(string="Tile Name", required=True, copy=False)
    link = fields.Char(string="Tile Link", required=True, copy=False)
    tile_active = fields.Boolean(string='Active', default=True)
    dynamic_link = fields.Boolean(string='Dynamic Link', default=True)
    icon = fields.Binary("Icon")
    tile_background_color_1 = fields.Char(default="#fe5f75", help="Default background color of the dashboard tile",
                                          string="Tile Color #1")
    tile_background_color_2 = fields.Char(default="#fc9842", help="Default background color of the dashboard tile",
                                          string="Tile Color #2")
    tile_text_color = fields.Char(default="#000000", help="Default text color of the dashboard tile")
    sequence = fields.Integer(string='Sequence', default='_default_sequence')

    def _default_sequence(self):
        """Sort new records at the end of the list."""
        sequence = 0
        for record in self.search([]):
            sequence = max(sequence, record.sequence + 1)
            return sequence
