from odoo.addons.base_rest.controllers import main
from odoo.http import request
from odoo.exceptions import ValidationError

class GameResourceController(main.RestController):
    _root_path = '/api/v1/'
    _collection_name = 'game.resource.services'
    _default_auth = 'user'

    @route(['/game.resource', '/game.resource/<int:id>'], methods=['GET'])
    def get(self, id=None, **kwargs):
        domain = [('id', '=', id)] if id else []
        resources = request.env['game.resource'].search_read(domain)
        return {'status': 200, 'data': resources}

    @route(['/game.resource'], methods=['POST'])
    def create(self, **kwargs):
        try:
            data = request.jsonrequest.get('params', {}).get('data', {})
            resource = request.env['game.resource'].create(data)
            return {'status': 201, 'data': resource.read()[0]}
        except ValidationError as e:
            return {'status': 400, 'error': str(e)}

    @route(['/game.resource/<int:id>'], methods=['PUT'])
    def update(self, id, **kwargs):
        try:
            data = request.jsonrequest.get('params', {}).get('data', {})
            resource = request.env['game.resource'].browse(id)
            resource.write(data)
            return {'status': 200, 'data': resource.read()[0]}
        except Exception as e:
            return {'status': 400, 'error': str(e)}

    @route(['/game.resource/<int:id>'], methods=['DELETE'])
    def delete(self, id, **kwargs):
        try:
            resource = request.env['game.resource'].browse(id)
            resource.unlink()
            return {'status': 204}
        except Exception as e:
            return {'status': 400, 'error': str(e)}