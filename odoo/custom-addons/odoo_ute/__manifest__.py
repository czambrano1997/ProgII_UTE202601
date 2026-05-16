# manifest actualizado agregué mi nombre como "maintainer".

{
    'name': "Administración de la UTE",

    'summary': "Gestión de docentes, estudiantes, carreras, materias y cursos de la UTE",

    'description': """
        Módulo actualizado de la gestión académica para la Universidad UTE.
        
        Proyecto base desarrollado por Ing.Ceider Zambrano.
        Finalizado, actualizado y mantenido por Mathias Rochina.

        Ahora permite administrar:
        - Docentes y sus materias asignadas
        - Estudiantes y matrículas
        - Carreras universitarias
        - Materias por carrera
        - Cursos, horarios y cupos
    """,

    'author': "Ceider Zambrano",
    'maintainer': "Mathias Rochina",
    'website': "https://github.com/czambrano1997/ProgII_UTE202601",
    'license': 'LGPL-3',

    'category': 'Education',
    'version': '0.3',

    'depends': ['base'],

    'data': [
        'security/ute_group.xml',
        'security/ir.model.access.csv',
        'security/ute_rule.xml',
        'views/teacher.xml',
        'views/signature.xml',
        'views/career.xml',
        'views/student.xml',
        'views/course.xml',
        'views/menu.xml',
    ],

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}