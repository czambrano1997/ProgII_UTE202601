{
    'name': "Administración de la UTE",
    'summary': "Gestión de docentes y recursos de la UTE",
    'description': """
Funcionalidades del módulo de gestión de la UTE.
    """,
    'author': "Ceider Zambrano",
    'website': "https://gezaforge.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ute_group.xml',
        'security/ir.model.access.csv',
        'security/ute_rule.xml',
        'views/teacher.xml',
        'views/signature.xml',
        'views/odoo_models_views.xml',
        'views/menu.xml',
    ],
    'demo': [],
}

