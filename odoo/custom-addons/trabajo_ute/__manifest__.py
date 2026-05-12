{
    'name': "Transporte UTE",

    'summary': "Gestion del Transporte de la UTE",

    'description': """
Funcionalidades del gestor de transporte
    """,

    'author': "Luis Arias",
    'website': "https://TransportLA.com",

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
        'views/horarios.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}

