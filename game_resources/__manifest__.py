{
    'name': 'Game Resources Management',
    'version': '1.0',
    'summary': 'Module to manage game resources and player inventory',
    'description': """
        This module allows the management of game resources such as items, weapons, and skins.
        It integrates with Unity for synchronization of data.
    """,
    'author': 'ADI',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/resource_views.xml',
        'views/menu_views.xml',

    ],
    'installable': True,
    'application': True,
}
