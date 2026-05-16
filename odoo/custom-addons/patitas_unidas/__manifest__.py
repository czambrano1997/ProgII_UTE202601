# -*- coding: utf-8 -*-
{
    'name': 'Patitas Unidas',
    'version': '19.0.1.0.0',
    'category': 'Industries/Services',
    'summary': 'Gestión integral de adopción de mascotas',
    'description': """
        Módulo para la gestión completa del ciclo de adopción de mascotas:
        - Registro y seguimiento de mascotas
        - Hogares adoptivos / temporales
        - Adoptantes y solicitudes de adopción
        - Historial médico por mascota
        - Seguridad por roles: Usuario, Voluntario y Gestor
    """,
    'depends': ['base', 'mail'],
    'data': [
        # ── Seguridad (orden: grupos → accesos → reglas)
        'security/groups.xml',
        'security/ir.model.access.csv',                

        # ── Vistas (forms, lists, searches, actions)
        'views/mascota_views.xml',
        'views/adoptante_views.xml',
        'views/hogar_adoptivo_views.xml',
        'views/solicitud_adopcion_views.xml',
        'views/historial_medico_views.xml',

        # ── Menús (siempre al final, después de las actions)
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}