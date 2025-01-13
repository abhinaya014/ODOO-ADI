from odoo import models, fields, api
from odoo.tools import float_round


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

    def toggle_availability(self):
        for record in self:
            record.availability = not record.availability


class PlayerInventory(models.Model):
    _name = 'player.inventory'
    _description = 'Player Inventory'

    player_id = fields.Many2one('res.users', string='Player', required=True)
    resource_id = fields.Many2one('game.resource', string='Resource', required=True)
    purchase_date = fields.Datetime(string='Purchase Date', default=fields.Datetime.now)