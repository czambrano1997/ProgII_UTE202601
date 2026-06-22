# -*- coding: utf-8 -*-
{
    'name': 'Teatro',
    'version': '19.0.1.0.0',
    'summary': 'Gestión de teatro: obras, funciones y boletos',
    'description': """
        Módulo para administrar un sistema de teatro:
        - Obras de teatro
        - Funciones programadas
        - Venta de boletos y control de capacidad
    """,
    'author': 'Mi Empresa',
    'category': 'Services',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/obra.xml',
        'views/funcion.xml',
        'views/boleto.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
