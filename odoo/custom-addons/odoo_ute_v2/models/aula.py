from odoo import api, fields, models
from odoo.exceptions import ValidationError

from .validators import validar_texto


class OuAula(models.Model):
    _name = "ou.aula"
    _description = "Aula"
    _order = "edificio, name, id"

    name = fields.Char(
        string="Nombre",
        required=True,
        size=80,
        index=True,
    )

    edificio = fields.Char(
        string="Edificio",
        required=True,
        size=100,
    )

    capacidad = fields.Integer(
        string="Capacidad",
        required=True,
        default=1,
    )

    _sql_constraints = [
        (
            "ou_aula_nombre_edificio_unique",
            "unique(name, edificio)",
            "Ya existe un aula con ese nombre en ese edificio.",
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

        if isinstance(valores.get("edificio"), str):
            valores["edificio"] = valores["edificio"].strip()

    @api.constrains(
        "name",
        "edificio",
        "capacidad",
    )
    def _validar_datos(self):
        for registro in self:
            validar_texto(
                registro.name,
                "El nombre del aula",
                maximo=80,
            )
            validar_texto(
                registro.edificio,
                "El edificio",
            )

            if registro.capacidad <= 0:
                raise ValidationError(
                    "La capacidad debe ser un número entero "
                    "mayor que cero."
                )
