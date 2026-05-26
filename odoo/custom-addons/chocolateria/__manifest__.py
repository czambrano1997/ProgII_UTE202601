{
    'name': 'Chocolateria',
    'version': '1.0',
    'summary': 'Sistema de gestion de chocolateria',
    'description': 'Modulo de gestion para chocolateria',
    'author': 'Erick',
    'category': 'Sales',
    'depends': ['base', 'hr'],
    'data': [
        #'security/security.xml',
        #'security/ir.model.access.csv',


        'views/cliente_views.xml',
        'views/producto_views.xml',
        'views/pedido_views.xml',
        #'views/detalle_views.xml',
        'views/empleado_views.xml',

        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}