from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Students(models.Model):
    _name = 'students.ute'
    _description = 'Estudiantes UTE'

    name = fields.Char(
        string='Nombres',
        required=True
    )

    surnames = fields.Char(
        string='Apellidos',
        required=True
    )

    full_name = fields.Char(
        string='Nombre Completo',
        compute='_compute_full_name',
        store=True
    )

    age = fields.Integer(
        string='Edad',
        required=True,
        default=18
    )

    phone = fields.Char(  # Cambiado a Char para conservar el '0' inicial
        string='Teléfono',
        required=True
    )

    vat = fields.Char(
        string="CI/RUC",
        required=True,
        size=13
    )

    grade_ids = fields.One2many(
        comodel_name='grade.line',
        inverse_name='student_id',
        string='Notas'
    )

    @api.depends('name', 'surnames')  # Corregido: 'name' en lugar de 'names'
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = f"{rec.name or ''} {rec.surnames or ''}".strip()

    @api.onchange('vat')
    def _onchange_vat(self):
        if self.vat and len(self.vat) < 10:
            return {
                'warning': {
                    'title': 'Advertencia',
                    'message': 'La CI/RUC debe tener al menos 10 o 13 caracteres'
                }
            }

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age and rec.age < 17:
                raise ValidationError("El estudiante debe ser mayor de 17 años")