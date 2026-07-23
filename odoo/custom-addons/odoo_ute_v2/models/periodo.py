from odoo import api, fields, models
from odoo.exceptions import ValidationError

from .validators import validar_periodo


class OuPeriodo(models.Model):
    _name = "ou.periodo"
    _description = "Periodo académico"
    _order = "fecha_inicio desc, id desc"

    name = fields.Char(
        string="Nombre",
        required=True,
        size=6,
        index=True,
    )

    fecha_inicio = fields.Date(
        string="Fecha de inicio",
        required=True,
    )

    fecha_fin = fields.Date(
        string="Fecha de fin",
        required=True,
    )

    activo = fields.Boolean(
        string="Activo",
        default=True,
    )

    _sql_constraints = [
        (
            "ou_periodo_name_unique",
            "unique(name)",
            "Ya existe un periodo académico con ese nombre.",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for valores in vals_list:
            if isinstance(valores.get("name"), str):
                valores["name"] = valores["name"].strip()

        return super().create(vals_list)

    def write(self, valores):
        if isinstance(valores.get("name"), str):
            valores["name"] = valores["name"].strip()

        return super().write(valores)

    @api.constrains(
        "name",
        "fecha_inicio",
        "fecha_fin",
    )
    def _validar_datos(self):
        for registro in self:
            validar_periodo(registro.name)

            if (
                registro.fecha_inicio
                and registro.fecha_fin
                and registro.fecha_fin < registro.fecha_inicio
            ):
                raise ValidationError(
                    "La fecha final no puede ser anterior "
                    "a la fecha inicial."
                )
