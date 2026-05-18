# -*- coding: utf-8 -*-
{
    'name': "Indicadores de Calificación UTE",

    'summary': "Gestión de indicadores y calificaciones del transporte UTE",

    'description': """
        Módulo para la gestión de indicadores de calificación de conductores y vehículos.
        Incluye evaluaciones por período, categorías de indicadores y reportes de calificación.
    """,

    'author': "Luis Arias",
    'website': "https://TransportLA.com",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': ['base', 'mail'],

    'data': [
        'security/ute_group.xml',
        'security/ir.model.access.csv',
        'views/indicador_categoria_views.xml',
        'views/periodo_evaluacion_views.xml',
        'views/calificacion_conductor_views.xml',
        'views/calificacion_vehiculo_views.xml',
        'views/reporte_calificacion_views.xml',
        'views/menu.xml',
    ],

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

