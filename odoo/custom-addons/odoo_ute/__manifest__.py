# -*- coding: utf-8 -*-
{
    'name': "Puesto De Comida",

    'summary': "Gestión integral de un puesto de comida rápida",

    'description': """
    Módulo para el control de pedidos, platillos, clientes e ingredientes.
    """,

    'author': "maty",
    'website': "https://Puesto De Comida.com",

    'category': 'Tools',
    'version': '19.0.1.0.0',

    # Cualquier módulo necesario para que este funcione correctamente
    'depends': ['base'],

    # Siempre cargados en este orden estricto (Seguridad primero, luego vistas)
    'data': [
        'security/comida_security.xml',
        'security/ir.model.access.csv',
        'views/odoomaty_proyecto_puesto_de_comida_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}