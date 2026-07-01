from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GestionProfesor(models.Model):
    _name = 'gestion.profesor'
    _description = 'Profesor'

    nombres = fields.Char(string='Nombres', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)

    name = fields.Char(
        string='Nombre completo',
        compute='_compute_name',
        store=True
    )

    cedula = fields.Char(string='Cédula', required=True)
    especialidad = fields.Char(string='Especialidad')
    email = fields.Char(string='Correo')
    telefono = fields.Char(string='Teléfono')
    salario = fields.Float(string='Salario')
    activo = fields.Boolean(string='Activo', default=True)

    materia_ids = fields.One2many(
        'gestion.materia',
        'profesor_id',
        string='Materias'
    )

    total_materias = fields.Integer(
        string='Total de materias',
        compute='_compute_total_materias',
        store=True
    )

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.nombres or ''} {record.apellidos or ''}".strip()

    @api.depends('materia_ids')
    def _compute_total_materias(self):
        for record in self:
            record.total_materias = len(record.materia_ids)

    @api.constrains('salario')
    def _check_salario(self):
        for record in self:
            if record.salario and record.salario < 0:
                raise ValidationError('El salario no puede ser negativo.')

    @api.constrains('cedula')
    def _check_cedula(self):
        for record in self:
            if record.cedula:
                if not record.cedula.isdigit():
                    raise ValidationError('La cédula del profesor debe contener solo números.')
                if len(record.cedula) != 10:
                    raise ValidationError('La cédula del profesor debe tener exactamente 10 dígitos.')

    @api.constrains('telefono')
    def _check_telefono(self):
        for record in self:
            if record.telefono:
                if not record.telefono.isdigit():
                    raise ValidationError('El celular del profesor debe contener solo números.')
                if len(record.telefono) != 10:
                    raise ValidationError('El celular del profesor debe tener exactamente 10 dígitos.')