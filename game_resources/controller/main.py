from odoo import http, fields
from odoo.http import request
import json

class GameAPIController(http.Controller):
    @http.route(['/api/v1/player/login'], type='json', auth='none', methods=['POST'], csrf=False)
    def player_login(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            username = data.get('username')
            password = data.get('password')
            
            player = request.env['game.player'].sudo().search([
                ('name', '=', username),
                ('password', '=', password),
                ('active', '=', True)
            ], limit=1)
            
            if player:
                player.sudo().write({'last_login': fields.Datetime.now()})
                return {
                    'status': 'success',
                    'data': {
                        'player_id': player.id,
                        'username': player.name,
                        'level': player.level,
                        'experience': player.experience
                    }
                }
            return {'status': 'error', 'message': 'Invalid credentials'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route(['/api/v1/player/<int:player_id>/inventory'], type='http', auth='none', methods=['GET'], csrf=False)
    def get_player_inventory(self, player_id):
        try:
            inventory = request.env['player.inventory'].sudo().search_read([
                ('player_id', '=', player_id)
            ], ['resource_id', 'quantity', 'acquisition_date', 'state'])
            
            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'data': inventory
                }),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                headers=[('Content-Type', 'application/json')]
            )

    @http.route(['/api/v1/match/create'], type='json', auth='none', methods=['POST'], csrf=False)
    def create_match(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            match = request.env['game.match'].sudo().create({
                'match_type': data.get('match_type'),
                'player_ids': [(6, 0, data.get('player_ids', []))],
                'state': 'draft'
            })
            return {
                'status': 'success',
                'data': {
                    'match_id': match.id,
                    'name': match.name
                }
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route(['/api/v1/match/<int:match_id>/end'], type='json', auth='none', methods=['POST'], csrf=False)
    def end_match(self, match_id, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            match = request.env['game.match'].sudo().browse(match_id)
            
            if match.state == 'finished':
                return {'status': 'error', 'message': 'Match already finished'}
                
            match.write({
                'winner_id': data.get('winner_id'),
                'score': data.get('score'),
                'state': 'finished',
                'end_time': fields.Datetime.now()
            })
            
            return {
                'status': 'success',
                'message': 'Match ended successfully',
                'data': {
                    'match_id': match.id,
                    'winner_id': match.winner_id.id,
                    'score': match.score
                }
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route(['/api/v1/resources'], type='http', auth='none', methods=['GET'], csrf=False)
    def get_resources(self):
        try:
            resources = request.env['game.resource'].sudo().search_read(
                [('availability', '=', True)],
                ['name', 'description', 'category', 'price']
            )
            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'data': resources
                }),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                headers=[('Content-Type', 'application/json')]
            )