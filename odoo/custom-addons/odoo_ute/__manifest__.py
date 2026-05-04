{
    'name': "Administración de la UTE",

    'summary': "Gestión de docentes y estudiantes de la UTE",

    'description': """
	Funcionalidades del módulo de gestión de la UTE.
    """,

    'author': "Ceider Zambrano",
    'website': "https://gezaforge.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/teacher.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}

