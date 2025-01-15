from odoo import http
from odoo.http import request

class GameController(http.Controller):
    @http.route('/game/players', auth='public', methods=['GET'], type='json', csrf=False)
    def list_players(self):
        players = request.env['game.player'].search([])
        return [{'id': p.id, 'name': p.name, 'level': p.level} for p in players]

    @http.route('/game/players', auth='public', methods=['POST'], type='json', csrf=False)
    def create_player(self, **kwargs):
        new_player = request.env['game.player'].create(kwargs)
        return {'id': new_player.id, 'name': new_player.name}

    @http.route('/game/players/<int:player_id>', auth='public', methods=['PUT'], type='json', csrf=False)
    def update_player(self, player_id, **kwargs):
        player = request.env['game.player'].browse(player_id)
        if player.exists():
            player.write(kwargs)
            return {'message': 'Player updated successfully'}
        return {'error': 'Player not found'}, 404

    @http.route('/game/players/<int:player_id>', auth='public', methods=['DELETE'], type='json', csrf=False)
    def delete_player(self, player_id):
        player = request.env['game.player'].browse(player_id)
        if player.exists():
            player.unlink()
            return {'message': 'Player deleted successfully'}
        return {'error': 'Player not found'}, 404
