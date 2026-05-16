# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Alumno(models.Model):
    _name = 'odoo_ute_v2.alumno'
    _description = 'Alumno'
    _rec_name = 'name'
    _order = 'apellido, nombre'

    name = fields.Char(
        string='Nombre completo',
        compute='_compute_name',
        store=True,
        index=True,
    )
    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    email = fields.Char(string='Email', index=True)
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
    active = fields.Boolean(string='Activo', default=True)

    calificacion_ids = fields.One2many(
        'odoo_ute_v2.calificacion', 'alumno_id', string='Calificaciones'
    )
    asistencia_ids = fields.One2many(
        'odoo_ute_v2.asistencia', 'alumno_id', string='Asistencias'
    )

    promedio = fields.Float(
        string='Promedio general',
        compute='_compute_promedio',
        store=True,
        digits=(4, 2),
    )
    porcentaje_asistencia = fields.Float(
        string='% Asistencia',
        compute='_compute_porcentaje_asistencia',
        store=True,
        digits=(5, 2),
    )

    @api.depends('nombre', 'apellido')
    def _compute_name(self):
        for r in self:
            partes = [p for p in [r.apellido, r.nombre] if p]
            r.name = ', '.join(partes) if partes else _('Sin nombre')

    @api.depends('calificacion_ids.nota')
    def _compute_promedio(self):
        for r in self:
            notas = r.calificacion_ids.mapped('nota')
            r.promedio = sum(notas) / len(notas) if notas else 0.0

    @api.depends('asistencia_ids.presente')
    def _compute_porcentaje_asistencia(self):
        for r in self:
            total = len(r.asistencia_ids)
            presentes = len(r.asistencia_ids.filtered(lambda a: a.presente))
            r.porcentaje_asistencia = (presentes / total * 100) if total else 0.0

    @api.constrains('email')
    def _validar_email(self):
        for r in self:
            if r.email and '@' not in r.email:
                raise ValidationError(_('El correo electrónico no tiene un formato válido.'))

    _alumno_email_unico = models.Constraint(
        'UNIQUE(email)',
        'Ya existe un alumno registrado con ese correo.',
    )
