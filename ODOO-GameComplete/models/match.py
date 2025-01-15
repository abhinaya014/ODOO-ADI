from odoo import models, fields

class Match(models.Model):
    _name = 'game.match'
    _description = 'Match'

    name = fields.Char(required=True)
    date = fields.Date(default=fields.Date.today)
    players_ids = fields.Many2many('game.player', string='Players')
    winner_id = fields.Many2one('game.player', string='Winner')
