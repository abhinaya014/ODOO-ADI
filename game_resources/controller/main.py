from odoo import http
from odoo import fields
from odoo.addons.base_rest.controllers import main
from odoo.http import request
from odoo.exceptions import ValidationError
import werkzeug.wrappers
import json

class GameAPIController(main.RestController):
    _root_path = '/api/v1/'
    _collection_name = 'game.api.services'
    _default_auth = 'user'

    # Player endpoints
    @http.route(['/api/player/login'], type='json', auth='none', methods=['POST'])
    def player_login(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            username = data.get('username')
            password = data.get('password')
            
            player = request.env['game.player'].sudo().search([
                ('name', '=', username),
                ('password', '=', password),
                ('active', '=', True)
            ])
            
            if player:
                player.write({'last_login': fields.Datetime.now()})
                return {
                    'status': 200,
                    'player_id': player.id,
                    'username': player.name,
                    'level': player.level,
                    'experience': player.experience
                }
            return {'status': 401, 'message': 'Invalid credentials'}
        except Exception as e:
            return {'status': 500, 'message': str(e)}

    @http.route(['/api/player/<int:player_id>/inventory'], type='http', auth='none', methods=['GET'])
    def get_player_inventory(self, player_id, **kwargs):
        try:
            inventory = request.env['player.inventory'].sudo().search_read([
                ('player_id', '=', player_id)
            ])
            return werkzeug.wrappers.Response(
                json.dumps({'status': 200, 'data': inventory}),
                mimetype='application/json'
            )
        except Exception as e:
            return werkzeug.wrappers.Response(
                json.dumps({'status': 500, 'error': str(e)}),
                mimetype='application/json'
            )

    # Match endpoints
    @http.route(['/api/match/create'], type='json', auth='none', methods=['POST'])
    def create_match(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            match = request.env['game.match'].sudo().create({
                'match_type': data.get('match_type'),
                'player_ids': [(6, 0, data.get('player_ids', []))],
                'state': 'draft'
            })
            return {'status': 201, 'match_id': match.id}
        except Exception as e:
            return {'status': 500, 'message': str(e)}

    @http.route(['/api/match/<int:match_id>/end'], type='json', auth='none', methods=['POST'])
    def end_match(self, match_id, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            match = request.env['game.match'].sudo().browse(match_id)
            match.write({
                'winner_id': data.get('winner_id'),
                'score': data.get('score'),
                'state': 'finished',
                'end_time': fields.Datetime.now()
            })
            return {'status': 200, 'message': 'Match ended successfully'}
        except Exception as e:
            return {'status': 500, 'message': str(e)}