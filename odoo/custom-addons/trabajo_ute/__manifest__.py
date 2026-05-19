# -*- coding: utf-8 -*-
{
    'name': "Indicadores de Calificación UTE",
    'summary': "Gestión de indicadores y calificaciones del transporte UTE",
    'description': """
        Módulo para la gestión de indicadores de calificación de conductores y vehículos.
    """,
    'author': "Luis Arias",
    'website': "https://TransportLA.com",
    'category': 'Human Resources',
    'version': '1.0',
    
    # DEPENDENCIAS - Agregar 'trabajo_ute' para acceder a ou.conductores y ou.rutas
    'depends': ['base', 'mail', 'trabajo_ute'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/indicador_categoria_views.xml',
        'views/periodo_evaluacion_views.xml',
        'views/calificacion_conductor_views.xml',
        'views/calificacion_vehiculo_views.xml',
        'views/reporte_calificacion_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}