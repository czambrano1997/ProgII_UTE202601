# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Asistencia(models.Model):
    _name = 'odoo_ute_v2.asistencia'
    _description = 'Asistencia'
    _rec_name = 'name'
    _order = 'fecha desc'

    name = fields.Char(
        string='Referencia',
        compute='_compute_name',
        store=True,
        index=True,
    )

    alumno_id = fields.Many2one(
        'odoo_ute_v2.alumno',
        string='Alumno',
        required=True,
        ondelete='cascade',
        index=True,
    )
    curso_id = fields.Many2one(
        'odoo_ute_v2.cursos',
        string='Curso',
        required=True,
        ondelete='restrict',
        index=True,
    )
    fecha = fields.Date(
        string='Fecha',
        required=True,
        default=fields.Date.today,
        index=True,
    )
    presente = fields.Boolean(
        string='Presente',
        default=True,
    )
    observaciones = fields.Text(string='Observaciones')

    @api.depends('alumno_id', 'curso_id', 'fecha')
    def _compute_name(self):
        for r in self:
            alumno = r.alumno_id.name if r.alumno_id else '?'
            curso = r.curso_id.nombre if r.curso_id else '?'
            fecha = r.fecha.strftime('%Y-%m-%d') if r.fecha else '?'
            r.name = f'{alumno} — {curso} ({fecha})'

    _asistencia_unica = models.Constraint(
        'UNIQUE(alumno_id, curso_id, fecha)',
        'Ya existe un registro de asistencia para este alumno en este curso en esa fecha.',
    )
