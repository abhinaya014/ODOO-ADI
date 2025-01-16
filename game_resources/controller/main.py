from odoo import http
from odoo.http import request
import json


class GameAPI(http.Controller):

    @http.route('/game/register', type='json', auth='public', methods=['POST'], csrf=False)
    def register_player(self, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not name or not email or not password:
            return {'status': 'error', 'message': 'Missing fields'}

        existing_user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
        if existing_user:
            return {'status': 'error', 'message': 'Player already exists'}

        user = request.env['res.users'].sudo().create({
            'name': name,
            'login': email,
            'password': password,
            'is_game_player': True
        })
        return {'status': 'success', 'player_id': user.id}

    @http.route('/game/login', type='json', auth='public', methods=['POST'], csrf=False)
    def login_player(self, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return {'status': 'error', 'message': 'Missing fields'}

        user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
        if not user or not user._check_password(password):
            return {'status': 'error', 'message': 'Invalid credentials'}

        return {'status': 'success', 'player_id': user.id}

    @http.route('/game/inventory', type='json', auth='user', methods=['GET'], csrf=False)
    def get_inventory(self):
        player = request.env.user
        if not player.is_game_player:
            return {'status': 'error', 'message': 'Access denied'}

        inventory = player.inventory.mapped(lambda item: {
            'resource_name': item.resource_id.name,
            'category': item.resource_id.category,
            'purchase_date': item.purchase_date
        })
        return {'status': 'success', 'inventory': inventory}

    @http.route('/game/match', type='json', auth='user', methods=['POST'], csrf=False)
    def create_match(self, **kwargs):
        player = request.env.user
        if not player.is_game_player:
            return {'status': 'error', 'message': 'Access denied'}

        match_name = kwargs.get('name')
        if not match_name:
            return {'status': 'error', 'message': 'Match name is required'}

        match = request.env['game.match'].sudo().create({
            'name': match_name,
            'player_id': player.id,
            'result': 'draw'
        })
        return {'status': 'success', 'match_id': match.id}

    @http.route('/game/match/<int:match_id>/finish', type='json', auth='user', methods=['POST'], csrf=False)
    def finish_match(self, match_id, **kwargs):
        player = request.env.user
        if not player.is_game_player:
            return {'status': 'error', 'message': 'Access denied'}

        match = request.env['game.match'].sudo().browse(match_id)
        if not match.exists():
            return {'status': 'error', 'message': 'Match not found'}

        match.result = kwargs.get('result', 'draw')
        match.end_time = fields.Datetime.now()
        return {'status': 'success', 'message': 'Match finished successfully'}