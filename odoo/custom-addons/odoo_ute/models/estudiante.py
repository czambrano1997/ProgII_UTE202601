from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class GestionEstudiante(models.Model):
    _name = 'gestion.estudiante'
    _description = 'Estudiante'

    nombres = fields.Char(string='Nombres', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)

    name = fields.Char(
        string='Nombre completo',
        compute='_compute_name',
        store=True
    )

    cedula = fields.Char(string='Cédula', required=True)
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
    edad = fields.Integer(string='Edad')
    email = fields.Char(string='Correo')
    telefono = fields.Char(string='Teléfono')
    activo = fields.Boolean(string='Activo', default=True)

    genero = fields.Selection([
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro'),
    ], string='Género')

    observaciones = fields.Text(string='Observaciones')

    matricula_ids = fields.One2many(
        'gestion.matricula',
        'estudiante_id',
        string='Matrículas'
    )

    total_matriculas = fields.Integer(
        string='Total de matrículas',
        compute='_compute_total_matriculas',
        store=True
    )

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.nombres or ''} {record.apellidos or ''}".strip()

    @api.depends('matricula_ids')
    def _compute_total_matriculas(self):
        for record in self:
            record.total_matriculas = len(record.matricula_ids)

    @api.onchange('fecha_nacimiento')
    def _onchange_fecha_nacimiento(self):
        if self.fecha_nacimiento:
            hoy = fields.Date.today()
            self.edad = relativedelta(hoy, self.fecha_nacimiento).years
        else:
            self.edad = 0

    @api.constrains('fecha_nacimiento')
    def _check_fecha_nacimiento(self):
        for record in self:
            if record.fecha_nacimiento and record.fecha_nacimiento > fields.Date.today():
                raise ValidationError('La fecha de nacimiento no puede ser futura.')

    @api.constrains('edad')
    def _check_edad(self):
        for record in self:
            if record.edad and record.edad < 0:
                raise ValidationError('La edad no puede ser negativa.')

    @api.constrains('cedula')
    def _check_cedula(self):
        for record in self:
            if record.cedula:
                if not record.cedula.isdigit():
                    raise ValidationError('La cédula debe contener solo números.')
                if len(record.cedula) != 10:
                    raise ValidationError('La cédula debe tener exactamente 10 dígitos.')

    @api.constrains('telefono')
    def _check_telefono(self):
        for record in self:
            if record.telefono:
                if not record.telefono.isdigit():
                    raise ValidationError('El celular debe contener solo números.')
                if len(record.telefono) != 10:
                    raise ValidationError('El celular debe tener exactamente 10 dígitos.')