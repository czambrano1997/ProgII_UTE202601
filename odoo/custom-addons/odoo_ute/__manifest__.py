{
    'name': "Administración de la UTE",

    'summary': "Gestión de docentes y estudiantes de la UTE",

    'description': """
	Funcionalidades del módulo de gestión de la UTE.
    """,

<<<<<<< HEAD
    'author': "alissonormaza",
    'website': "https://www.yourcompany.com",
=======
    'author': "Ceider Zambrano",
    'website': "https://gezaforge.com",
>>>>>>> 429d1272c840b1f1bfce85079b1d2e792e7e9351

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_managements'],

    # always loaded
    'data': [
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
    ],
}

