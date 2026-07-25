{
    'name': "Administración de la UTE",
    'summary': "Gestión de docentes, materias, carreras, períodos y aulas de la UTE",
    'description': """
        Funcionalidades del módulo de gestión de la UTE.
        Incluye modelos para docentes, materias, carreras, períodos académicos y aulas.
        Expone 15 endpoints HTTP para integración con Django.
    """,
    'author': "Ceider Zambrano",
    'website': "https://gezaforge.com",
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ute_group.xml',
        'security/ir.model.access.csv',
        'security/ute_rule.xml',
        'views/teacher.xml',
        'views/signature.xml',
        'views/carrera_views.xml',
        'views/periodo_views.xml',
        'views/aula_views.xml',
        'views/menu.xml',
    ],
    'demo': [],
}
