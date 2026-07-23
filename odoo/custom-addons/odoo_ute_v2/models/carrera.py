from odoo import api, fields, models

from .validators import validar_codigo, validar_texto


class OuCarrera(models.Model):
    _name = "ou.carrera"
    _description = "Carrera"
    _order = "name, id"

    name = fields.Char(
        string="Nombre",
        required=True,
        size=100,
        index=True,
    )

    codigo = fields.Char(
        string="Código",
        required=True,
        size=15,
        index=True,
    )

    modalidad = fields.Selection(
        [
            ("presencial", "Presencial"),
            ("virtual", "Virtual"),
            ("hibrida", "Híbrida"),
        ],
        string="Modalidad",
        required=True,
        default="presencial",
    )

    _sql_constraints = [
        (
            "ou_carrera_codigo_unique",
            "unique(codigo)",
            "Ya existe una carrera con ese código.",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for valores in vals_list:
            self._normalizar_valores(valores)

        return super().create(vals_list)

    def write(self, valores):
        self._normalizar_valores(valores)
        return super().write(valores)

    @staticmethod
    def _normalizar_valores(valores):
        if isinstance(valores.get("name"), str):
            valores["name"] = valores["name"].strip()

        if isinstance(valores.get("codigo"), str):
            valores["codigo"] = valores["codigo"].strip().upper()

    @api.constrains("name", "codigo")
    def _validar_datos(self):
        for registro in self:
            validar_texto(
                registro.name,
                "El nombre de la carrera",
            )
            validar_codigo(registro.codigo)
