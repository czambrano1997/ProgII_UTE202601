{
    "name": "UTE Complementos Academicos",
    "summary": "Modelos complementarios para el modulo Administracion de la UTE",
    "description": """
        Complementa el modulo odoo_ute con planificacion docente, aulas,
        horarios, asistencias y evaluaciones academicas.
    """,
    "author": "Jacome Jandry",
    "website": "https://github.com/czambrano1997/ProgII_UTE202601",
    "category": "Education",
    "version": "1.0",
    "depends": ["odoo_ute"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "security/record_rules.xml",
        "views/teacher_extension_views.xml",
        "views/academic_plan_views.xml",
        "views/classroom_views.xml",
        "views/class_schedule_views.xml",
        "views/attendance_views.xml",
        "views/teacher_evaluation_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
