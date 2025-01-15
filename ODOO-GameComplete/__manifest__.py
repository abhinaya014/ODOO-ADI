
{
    'name': 'Game Complete Module',
    'version': '1.0',
    'summary': 'Complete module for game management: players, matches, and inventory',
    'description': 'Includes full functionality with models, views, controllers, and security for Postman CRUD operations.',
    'author': 'ChatGPT',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/player_views.xml',
        'views/match_views.xml',
        'views/inventory_views.xml'
    ],
    'installable': True,
    'application': True,
}
