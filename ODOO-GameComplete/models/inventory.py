from odoo import models, fields

class Inventory(models.Model):
    _name = 'game.inventory'
    _description = 'Inventory'

    name = fields.Char(required=True)
    type = fields.Selection([('weapon', 'Weapon'), ('potion', 'Potion'), ('equipment', 'Equipment')], required=True)
    player_id = fields.Many2one('game.player', string='Player', ondelete='cascade')
    quantity = fields.Integer(default=1)
