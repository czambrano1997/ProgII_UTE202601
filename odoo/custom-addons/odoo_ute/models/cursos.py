# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Cursos(models.Model):
    _name = 'odoo_ute_v2.cursos'
    _description = 'Curso'
    _rec_name = 'nombre'
    _order = 'nombre'

    nombre = fields.Char(string='Nombre del curso', required=True, index=True)
    descripcion = fields.Text(string='Descripción')
    creditos = fields.Integer(string='Créditos', default=3)
    active = fields.Boolean(string='Activo', default=True)

    maestro_id = fields.Many2one(
        'odoo_ute_v2.maestro',
        string='Maestro',
        required=True,
        ondelete='restrict',
        index=True,
    )

    calificacion_ids = fields.One2many(
        'odoo_ute_v2.calificacion', 'curso_id', string='Calificaciones'
    )
    asistencia_ids = fields.One2many(
        'odoo_ute_v2.asistencia', 'curso_id', string='Registros de asistencia'
    )

    num_calificaciones = fields.Integer(
        string='N° Calificaciones',
        compute='_compute_num_calificaciones',
        store=True,
    )
    promedio_curso = fields.Float(
        string='Promedio del curso',
        compute='_compute_promedio_curso',
        store=True,
        digits=(4, 2),
    )

    @api.depends('calificacion_ids')
    def _compute_num_calificaciones(self):
        for r in self:
            r.num_calificaciones = len(r.calificacion_ids)

    @api.depends('calificacion_ids.nota')
    def _compute_promedio_curso(self):
        for r in self:
            notas = r.calificacion_ids.mapped('nota')
            r.promedio_curso = sum(notas) / len(notas) if notas else 0.0

    @api.constrains('creditos')
    def _validar_creditos(self):
        for r in self:
            if r.creditos < 1:
                raise ValidationError(_('Los créditos del curso deben ser al menos 1.'))
