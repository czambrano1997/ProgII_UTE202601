from odoo import api, fields, models

from .validators import (
    validar_email,
    validar_identificacion,
    validar_persona,
    validar_telefono,
)


class SistemaUsuarios(models.Model):
    _name = "sistema.usuarios"
    _description = "Docente"
    _order = "last_name, name, id"

    name = fields.Char(
        string="Nombres",
        required=True,
        size=80,
        index=True,
    )

    last_name = fields.Char(
        string="Apellidos",
        required=True,
        size=80,
        index=True,
    )

    email = fields.Char(
        string="Correo electrónico",
        required=True,
        size=120,
        index=True,
    )

    phone = fields.Char(
        string="Teléfono",
        required=True,
        size=10,
    )

    vat = fields.Char(
        string="Cédula ecuatoriana",
        required=True,
        size=10,
        index=True,
    )

    _sql_constraints = [
        (
            "sistema_usuarios_email_unique",
            "unique(email)",
            "Ya existe un docente con ese correo electrónico.",
        ),
        (
            "sistema_usuarios_vat_unique",
            "unique(vat)",
            "Ya existe un docente con esa cédula.",
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
        """
        Limpia y normaliza datos antes de guardarlos.
        """
        for campo in (
            "name",
            "last_name",
            "phone",
            "vat",
        ):
            if isinstance(valores.get(campo), str):
                valores[campo] = valores[campo].strip()

        if isinstance(valores.get("email"), str):
            valores["email"] = (
                valores["email"]
                .strip()
                .lower()
            )

    @api.constrains(
        "name",
        "last_name",
        "email",
        "phone",
        "vat",
    )
    def _validar_datos(self):
        """
        Validación definitiva del lado de Odoo.

        Se ejecuta al crear o modificar desde:
        - La interfaz de Odoo
        - Los controladores HTTP
        - Código Python
        """
        for registro in self:
            validar_persona(
                registro.name,
                "Los nombres",
            )

            validar_persona(
                registro.last_name,
                "Los apellidos",
            )

            validar_email(
                registro.email,
            )

            validar_telefono(
                registro.phone,
            )

            validar_identificacion(
                registro.vat,
            )
