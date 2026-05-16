# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Calificacion(models.Model):
    _name = 'odoo_ute_v2.calificacion'
    _description = 'Calificación'
    _rec_name = 'name'
    _order = 'fecha_evaluacion desc'

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
    nota = fields.Float(
        string='Nota',
        required=True,
        digits=(4, 2),
        help='Escala 0 – 10',
    )
    tipo_evaluacion = fields.Selection(
        [
            ('parcial',    'Examen parcial'),
            ('final',      'Examen final'),
            ('tarea',      'Tarea'),
            ('proyecto',   'Proyecto'),
            ('laboratorio','Laboratorio'),
            ('otro',       'Otro'),
        ],
        string='Tipo de evaluación',
        required=True,
        default='parcial',
        index=True,
    )
    fecha_evaluacion = fields.Date(
        string='Fecha de evaluación',
        required=True,
        default=fields.Date.today,
        index=True,
    )
    observaciones = fields.Text(string='Observaciones')

    @api.depends('alumno_id', 'curso_id', 'tipo_evaluacion')
    def _compute_name(self):
        for r in self:
            alumno = r.alumno_id.name if r.alumno_id else '?'
            curso = r.curso_id.nombre if r.curso_id else '?'
            tipo = dict(r._fields['tipo_evaluacion'].selection).get(r.tipo_evaluacion, '')
            r.name = f'{alumno} — {curso} [{tipo}]'

    @api.constrains('nota')
    def _validar_nota(self):
        for r in self:
            if not (0.0 <= r.nota <= 10.0):
                raise ValidationError(_('La nota debe estar entre 0 y 10.'))
