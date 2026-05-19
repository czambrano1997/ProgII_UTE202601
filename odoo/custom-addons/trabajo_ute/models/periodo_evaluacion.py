# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class PeriodoEvaluacion(models.Model):
    _name = 'ou.periodo.evaluacion'
    _description = 'Período de Evaluación'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_inicio desc'

    name = fields.Char(string='Nombre del Período', required=True, tracking=True)
    code = fields.Char(string='Código', required=True, copy=False)
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True, tracking=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=True, tracking=True)
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_proceso', 'En Proceso'),
        ('cerrado', 'Cerrado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='borrador', tracking=True)
    active = fields.Boolean(string='Activo', default=True)
    descripcion = fields.Text(string='Descripción')
    
    # Campos computados
    duracion_dias = fields.Integer(
        string='Duración (Días)', 
        compute='_compute_duracion', 
        store=True
    )
    dias_restantes = fields.Integer(
        string='Días Restantes', 
        compute='_compute_dias_restantes'
    )
    es_vigente = fields.Boolean(
        string='Es Vigente', 
        compute='_compute_es_vigente', 
        store=True
    )
    
    # Campos relacionales
    calificacion_conductor_ids = fields.One2many(
        'ou.calificacion.conductor',
        'periodo_id',
        string='Calificaciones de Conductores'
    )
    total_calificaciones = fields.Integer(
        string='Total Calificaciones',
        compute='_compute_total_calificaciones',
        store=True
    )

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_duracion(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                record.duracion_dias = (record.fecha_fin - record.fecha_inicio).days
            else:
                record.duracion_dias = 0

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_dias_restantes(self):
        hoy = date.today()
        for record in self:
            if record.state == 'cerrado' or record.state == 'cancelado':
                record.dias_restantes = 0
            elif record.fecha_fin:
                diff = (record.fecha_fin - hoy).days
                record.dias_restantes = diff if diff > 0 else 0
            else:
                record.dias_restantes = 0

    @api.depends('fecha_inicio', 'fecha_fin', 'state')
    def _compute_es_vigente(self):
        hoy = date.today()
        for record in self:
            record.es_vigente = (
                record.state == 'en_proceso' and
                record.fecha_inicio <= hoy <= record.fecha_fin
            )

    @api.depends('calificacion_conductor_ids')
    def _compute_total_calificaciones(self):
        for record in self:
            record.total_calificaciones = len(record.calificacion_conductor_ids)

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                if record.fecha_inicio > record.fecha_fin:
                    raise ValidationError('La fecha de inicio no puede ser posterior a la fecha de fin.')

    @api.constrains('fecha_inicio', 'fecha_fin', 'state')
    def _check_periodo_unico(self):
        for record in self:
            if record.state == 'en_proceso':
                dominio = [
                    ('state', '=', 'en_proceso'),
                    ('id', '!=', record.id),
                    ('fecha_inicio', '<=', record.fecha_fin),
                    ('fecha_fin', '>=', record.fecha_inicio),
                ]
                if self.search_count(dominio) > 0:
                    raise ValidationError('No puede haber dos períodos en proceso con fechas superpuestas.')

    @api.onchange('fecha_inicio')
    def _onchange_fecha_inicio(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            self.fecha_fin = False
            return {'warning': {
                'title': 'Fechas inválidas',
                'message': 'La fecha de inicio no puede ser posterior a la fecha de fin.'
            }}

    def action_iniciar(self):
        for record in self:
            record.state = 'en_proceso'

    def action_cerrar(self):
        for record in self:
            record.state = 'cerrado'

    def action_cancelar(self):
        for record in self:
            record.state = 'cancelado'
<<<<<<< HEAD
=======

    _sql_constraints = [
        ('unique_periodo_code', 'UNIQUE(code)', 'El código del período debe ser único.'),
    ]
>>>>>>> c1b48e8873a20a5a1324a750d1a52238c1f0fcc6
