# -*- coding: utf-8 -*-
{
    'name': 'Gestión Académica UTE',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Gestión de alumnos, maestros, cursos, calificaciones y asistencias',
    'author': 'Isaac Betun',
    'depends': ['base'],
    'data': [
        # Seguridad
        'security/groups.xml',
        'security/ir.model.access.csv',

        # Vistas por modelo
        'views/maestro_views.xml',
        'views/alumno_views.xml',
        'views/cursos_views.xml',
        'views/calificacion_views.xml',
        'views/asistencia_views.xml',

        # Menú (siempre al final)
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
