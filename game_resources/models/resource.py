from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GamePlayer(models.Model):
    _name = 'game.player'
    _description = 'Game Player'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Username', required=True, tracking=True)
    email = fields.Char(string='Email', required=True)
    password = fields.Char(string='Password', required=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    level = fields.Integer(string='Level', default=1, tracking=True)
    experience = fields.Integer(string='Experience Points', default=0)
    last_login = fields.Datetime(string='Last Login')
    registration_date = fields.Date(string='Registration Date', default=fields.Date.today)
    inventory_ids = fields.One2many('player.inventory', 'player_id', string='Inventory')
    match_ids = fields.Many2many('game.match', 'player_match_rel', 'player_id', 'match_id', string='Matches')
    image = fields.Binary(string='Avatar', attachment=True)
    
    _sql_constraints = [
        ('unique_username', 'unique(name)', 'Username must be unique!'),
        ('unique_email', 'unique(email)', 'Email must be unique!')
    ]

class GameMatch(models.Model):
    _name = 'game.match'
    _description = 'Game Match'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_time desc'

    name = fields.Char(string='Match ID', required=True, copy=False, 
                      default=lambda self: self.env['ir.sequence'].next_by_code('game.match'))
    start_time = fields.Datetime(string='Start Time', tracking=True)
    end_time = fields.Datetime(string='End Time', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    player_ids = fields.Many2many('game.player', 'player_match_rel', 'match_id', 'player_id', 
                                 string='Players')
    winner_id = fields.Many2one('game.player', string='Winner', tracking=True)
    match_type = fields.Selection([
        ('duel', '1v1'),
        ('team', 'Team Match'),
        ('battle_royale', 'Battle Royale')
    ], string='Match Type', required=True, default='duel')
    score = fields.Integer(string='Score')
    notes = fields.Text(string='Match Notes')

    @api.constrains('player_ids')
    def _check_players_count(self):
        for match in self:
            if match.match_type == 'duel' and len(match.player_ids) != 2:
                raise ValidationError('Duel matches must have exactly 2 players!')
            elif match.match_type == 'team' and len(match.player_ids) != 4:
                raise ValidationError('Team matches must have exactly 4 players!')
            elif match.match_type == 'battle_royale' and len(match.player_ids) < 10:
                raise ValidationError('Battle Royale matches must have at least 10 players!')

    def action_start_match(self):
        self.ensure_one()
        self.write({
            'state': 'in_progress',
            'start_time': fields.Datetime.now()
        })

    def action_end_match(self):
        self.ensure_one()
        self.write({
            'state': 'finished',
            'end_time': fields.Datetime.now()
        })

    def action_cancel_match(self):
        self.write({'state': 'cancelled'})