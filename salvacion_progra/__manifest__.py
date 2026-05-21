{
    'name': 'Salvación Progra',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Módulo ultra simple de tareas',
    'depends': ['base'],
    'data': [
        'security/security_groups.xml',   # <-- DEBE IR PRIMERO (Crea los roles)
        'security/ir.model.access.csv',   # <-- DEBE IR SEGUNDO (Asigna los permisos)
        'views/vistas_proyecto.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}