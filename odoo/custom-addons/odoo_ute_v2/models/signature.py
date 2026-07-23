from odoo import api, fields, models
from odoo.exceptions import ValidationError

from .validators import validar_texto


class OuSignature(models.Model):
    _name = "ou.signature"
    _description = "Materia"
    _order = "name, id"

    name = fields.Char(
        string="Nombre",
        required=True,
        size=100,
        index=True,
    )

    _sql_constraints = [
        (
            "ou_signature_name_unique",
            "unique(name)",
            "Ya existe una materia con ese nombre.",
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

    @api.constrains("name")
    def _validar_name(self):
        for registro in self:
            validar_texto(
                registro.name,
                "El nombre de la materia",
            )

            duplicado = self.search_count(
                [
                    ("id", "!=", registro.id),
                    ("name", "=ilike", registro.name.strip()),
                ]
            )

            if duplicado:
                raise ValidationError(
                    "Ya existe una materia con ese nombre."
                )
