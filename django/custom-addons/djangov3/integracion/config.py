from collections import OrderedDict


MODELOS = OrderedDict({
    "signature": {
        "titulo": "Materias",
        "singular": "Materia",
        "campos": [
            {
                "name": "name",
                "label": "Nombre",
                "type": "text",
                "required": True,
                "min_length": 2,
                "max_length": 100,
            },
        ],
    },

    "usuarios": {
        "titulo": "Docentes",
        "singular": "Docente",
        "campos": [
            {
                "name": "name",
                "label": "Nombres",
                "type": "text",
                "required": True,
                "min_length": 2,
                "max_length": 80,
            },
            {
                "name": "last_name",
                "label": "Apellidos",
                "type": "text",
                "required": True,
                "min_length": 2,
                "max_length": 80,
            },
            {
                "name": "email",
                "label": "Correo electrónico",
                "type": "email",
                "required": True,
                "max_length": 120,
            },
            {
                "name": "phone",
                "label": "Teléfono",
                "type": "text",
                "required": True,
                "min_length": 10,
                "max_length": 10,
                "widget_attrs": {
                    "inputmode": "numeric",
                    "pattern": "0[0-9]{9}",
                    "maxlength": "10",
                    "placeholder": "0999999999",
                    "autocomplete": "tel",
                },
            },
            {
                "name": "vat",
                "label": "Cédula ecuatoriana",
                "type": "text",
                "required": True,
                "min_length": 10,
                "max_length": 10,
                "widget_attrs": {
                    "inputmode": "numeric",
                    "pattern": "[0-9]{10}",
                    "maxlength": "10",
                    "placeholder": "10 dígitos",
                    "autocomplete": "off",
                },
            },
        ],
    },

    "carrera": {
        "titulo": "Carreras",
        "singular": "Carrera",
        "campos": [
            {
                "name": "name",
                "label": "Nombre",
                "type": "text",
                "required": True,
                "min_length": 2,
                "max_length": 100,
            },
            {
                "name": "codigo",
                "label": "Código",
                "type": "text",
                "required": True,
                "min_length": 2,
                "max_length": 15,
            },
            {
                "name": "modalidad",
                "label": "Modalidad",
                "type": "choice",
                "required": True,
                "choices": [
                    (
                        "presencial",
                        "Presencial",
                    ),
                    (
                        "virtual",
                        "Virtual",
                    ),
                    (
                        "hibrida",
                        "Híbrida",
                    ),
                ],
            },
        ],
    },

    "periodo": {
        "titulo": "Periodos académicos",
        "singular": "Periodo académico",
        "campos": [
            {
                "name": "name",
                "label": "Nombre",
                "type": "text",
                "required": True,
                "min_length": 6,
                "max_length": 6,
                "widget_attrs": {
                    "placeholder": "2025-2",
                    "pattern": "[0-9]{4}-[12]",
                },
            },
            {
                "name": "fecha_inicio",
                "label": "Fecha de inicio",
                "type": "date",
                "required": True,
            },
            {
                "name": "fecha_fin",
                "label": "Fecha de fin",
                "type": "date",
                "required": True,
            },
            {
                "name": "activo",
                "label": "Activo",
                "type": "boolean",
                "required": False,
                "initial": True,
            },
        ],
    },

    "aula": {
        "titulo": "Aulas",
        "singular": "Aula",
        "campos": [
            {
                "name": "name",
                "label": "Nombre",
                "type": "text",
                "required": True,
                "min_length": 2,
                "max_length": 80,
            },
            {
                "name": "edificio",
                "label": "Edificio",
                "type": "text",
                "required": True,
                "min_length": 2,
                "max_length": 100,
            },
            {
                "name": "capacidad",
                "label": "Capacidad",
                "type": "integer",
                "required": True,
                "min_value": 1,
                "max_value": 10000,
            },
        ],
    },
})


def obtener_config(modelo):
    return MODELOS.get(modelo)
