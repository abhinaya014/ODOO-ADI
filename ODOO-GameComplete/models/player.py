from odoo import models, fields

class Player(models.Model):
    _name = 'game.player'
    _description = 'Player'

    name = fields.Char(required=True)
    email = fields.Char(required=True, unique=True)
    password = fields.Char(required=True)
    level = fields.Integer(default=1)
    experience = fields.Float(default=0.0)
    inventory_ids = fields.One2many('game.inventory', 'player_id', string='Inventory')
    match_ids = fields.Many2many('game.match', string='Matches')
