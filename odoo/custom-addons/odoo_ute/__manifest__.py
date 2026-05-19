{
<<<<<<< HEAD
    'name': "odoo_ute",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
=======
    'name': "Administración de la UTE",

    'summary': "Gestión de docentes y estudiantes de la UTE",

    'description': """
	Funcionalidades del módulo de gestión de la UTE.
    """,

    'author': "Ceider Zambrano",
    'website': "https://gezaforge.com",
>>>>>>> origin/docente/zambrano_ceider

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
<<<<<<< HEAD
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
=======
        'security/ute_group.xml',
        'security/ir.model.access.csv',
        'security/ute_rule.xml',
        'views/teacher.xml',
        'views/signature.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
>>>>>>> origin/docente/zambrano_ceider
    ],
}

