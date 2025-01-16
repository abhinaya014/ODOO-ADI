from odoo import models, fields, api


class GameResource(models.Model):
    _name = 'game.resource'
    _description = 'Game Resource'
    _order = 'name'

    name = fields.Char(string='Resource Name', required=True)
    description = fields.Text(string='Description')
    price = fields.Float(string='Price', required=True)
    category = fields.Selection([
        ('weapon', 'Weapon'),
        ('skin', 'Skin'),
        ('ability', 'Ability'),
    ], string='Category', required=True)
    availability = fields.Boolean(string='Available', default=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id.id)
    image = fields.Binary(string='Image', attachment=True)

    def toggle_availability(self):
        for record in self:
            record.availability = not record.availability


class PlayerInventory(models.Model):
    _name = 'player.inventory'
    _description = 'Player Inventory'

    player_id = fields.Many2one('res.users', string='Player', required=True)
    resource_id = fields.Many2one('game.resource', string='Resource', required=True)
    purchase_date = fields.Datetime(string='Purchase Date', default=fields.Datetime.now)


class GamePlayer(models.Model):
    _inherit = 'res.users'

    is_game_player = fields.Boolean(string='Is Game Player', default=False)
    matches_played = fields.One2many('game.match', 'player_id', string='Matches Played')
    inventory = fields.One2many('player.inventory', 'player_id', string='Inventory')



class GameMatch(models.Model):
    _name = 'game.match'
    _description = 'Game Match'

    name = fields.Char(string='Match Name', required=True)
    player_id = fields.Many2one('res.users', string='Player', required=True)
    start_time = fields.Datetime(string='Start Time', default=fields.Datetime.now)
    end_time = fields.Datetime(string='End Time')
    result = fields.Selection([
        ('win', 'Win'),
        ('lose', 'Lose'),
        ('draw', 'Draw'),
    ], string='Result', required=True)
