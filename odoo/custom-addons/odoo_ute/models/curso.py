from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GestionCurso(models.Model):
    _name = 'gestion.curso'
    _description = 'Curso'

    name = fields.Char(string='Nombre del curso', required=True)
    descripcion = fields.Text(string='Descripción')

    nivel = fields.Selection([
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ], string='Nivel', required=True)

    cupo_maximo = fields.Integer(string='Cupo máximo')
    fecha_inicio = fields.Date(string='Fecha de inicio')
    fecha_fin = fields.Date(string='Fecha de fin')
    activo = fields.Boolean(string='Activo', default=True)

    materia_ids = fields.One2many(
        'gestion.materia',
        'curso_id',
        string='Materias'
    )

    matricula_ids = fields.One2many(
        'gestion.matricula',
        'curso_id',
        string='Matrículas'
    )

    total_matriculados = fields.Integer(
        string='Total matriculados',
        compute='_compute_total_matriculados',
        store=True
    )

    @api.depends('matricula_ids')
    def _compute_total_matriculados(self):
        for record in self:
            record.total_matriculados = len(record.matricula_ids)

    @api.constrains('cupo_maximo')
    def _check_cupo_maximo(self):
        for record in self:
            if record.cupo_maximo and record.cupo_maximo <= 0:
                raise ValidationError('El cupo máximo debe ser mayor que cero.')