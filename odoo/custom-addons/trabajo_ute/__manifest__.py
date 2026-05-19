# -*- coding: utf-8 -*-
{
    'name': "Indicadores de Calificación UTE",
<<<<<<< HEAD
    'summary': "Gestión de indicadores y calificaciones del transporte UTE",
    'description': """
        Módulo para la gestión de indicadores de calificación de conductores y vehículos.
=======

    'summary': "Gestión de indicadores y calificaciones del transporte UTE",

    'description': """
        Módulo para la gestión de indicadores de calificación de conductores y vehículos.
        Incluye evaluaciones por período, categorías de indicadores y reportes de calificación.
>>>>>>> c1b48e8873a20a5a1324a750d1a52238c1f0fcc6
    """,
    'author': "Luis Arias",
    'website': "https://TransportLA.com",
    'category': 'Human Resources',
    'version': '1.0',
<<<<<<< HEAD
    
    # DEPENDENCIAS - Agregar 'trabajo_ute' para acceder a ou.conductores y ou.rutas
    'depends': ['base', 'mail', 'trabajo_ute'],

    'data': [
        'security/groups.xml',
=======
    'depends': ['base', 'mail'],

    'data': [
        'security/ute_group.xml',
>>>>>>> c1b48e8873a20a5a1324a750d1a52238c1f0fcc6
        'security/ir.model.access.csv',
        'views/indicador_categoria_views.xml',
        'views/periodo_evaluacion_views.xml',
        'views/calificacion_conductor_views.xml',
        'views/calificacion_vehiculo_views.xml',
        'views/reporte_calificacion_views.xml',
        'views/menu.xml',
    ],
<<<<<<< HEAD
    'installable': True,
    'application': True,
    'auto_install': False,
}
=======

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

>>>>>>> c1b48e8873a20a5a1324a750d1a52238c1f0fcc6
