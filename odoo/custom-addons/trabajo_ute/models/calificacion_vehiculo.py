# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CalificacionVehiculo(models.Model):
    _name = 'ou.calificacion.vehiculo'
    _description = 'Calificación de Vehículo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_evaluacion desc'

    name = fields.Char(string='Referencia', required=True, copy=False, default='Nuevo')
    periodo_id = fields.Many2one(
        'ou.periodo.evaluacion',
        string='Período de Evaluación',
        required=True,
        tracking=True
    )
    vehiculo_id = fields.Many2one(
        'ou.rutas',  # Asumiendo que rutas maneja vehículos, ajusta según tu modelo real
        string='Vehículo',
        required=True,
        tracking=True
    )
    conductor_asignado_id = fields.Many2one(
        'ou.conductores',
        string='Conductor Asignado'
    )
    fecha_evaluacion = fields.Date(string='Fecha de Evaluación', required=True, default=fields.Date.today)
    evaluador_id = fields.Many2one(
        'res.users',
        string='Evaluador',
        default=lambda self: self.env.user,
        required=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('calificado', 'Calificado'),
        ('revisado', 'Revisado'),
        ('aprobado', 'Aprobado'),
    ], string='Estado', default='borrador', tracking=True)
    observaciones = fields.Text(string='Observaciones')
    
    # Campos de calificación
    estado_mecanico = fields.Float(string='Estado Mecánico (0-10)', default=0.0)
    estado_exterior = fields.Float(string='Estado Exterior (0-10)', default=0.0)
    estado_interior = fields.Float(string='Estado Interior (0-10)', default=0.0)
    nivel_combustible = fields.Float(string='Nivel Combustible (0-10)', default=0.0)
    documentacion = fields.Float(string='Documentación (0-10)', default=0.0)
    kilometraje = fields.Float(string='Kilometraje Actual', default=0.0)
    
    # Campos computados
    puntaje_total = fields.Float(
        string='Puntaje Total',
        compute='_compute_puntaje_total',
        store=True
    )
    promedio = fields.Float(
        string='Promedio',
        compute='_compute_promedio',
        store=True
    )
    estado_general = fields.Selection([
        ('excelente', 'Excelente'),
        ('bueno', 'Bueno'),
        ('regular', 'Regular'),
        ('malo', 'Malo'),
        ('critico', 'Crítico'),
    ], string='Estado General', compute='_compute_estado_general', store=True)
    
    # Campos relacionales
    mantenimiento_ids = fields.One2many(
        'ou.vehiculo.mantenimiento',
        'calificacion_id',
        string='Registros de Mantenimiento'
    )
    total_mantenimientos = fields.Integer(
        string='Total Mantenimientos',
        compute='_compute_total_mantenimientos',
        store=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('ou.calificacion.vehiculo') or 'Nuevo'
        return super(CalificacionVehiculo, self).create(vals_list)

    @api.depends('estado_mecanico', 'estado_exterior', 'estado_interior', 
                 'nivel_combustible', 'documentacion')
    def _compute_puntaje_total(self):
        for record in self:
            record.puntaje_total = (
                record.estado_mecanico +
                record.estado_exterior +
                record.estado_interior +
                record.nivel_combustible +
                record.documentacion
            )

    @api.depends('puntaje_total')
    def _compute_promedio(self):
        for record in self:
            record.promedio = record.puntaje_total / 5.0

    @api.depends('promedio')
    def _compute_estado_general(self):
        for record in self:
            if record.promedio >= 9:
                record.estado_general = 'excelente'
            elif record.promedio >= 7.5:
                record.estado_general = 'bueno'
            elif record.promedio >= 6:
                record.estado_general = 'regular'
            elif record.promedio >= 4:
                record.estado_general = 'malo'
            else:
                record.estado_general = 'critico'

    @api.depends('mantenimiento_ids')
    def _compute_total_mantenimientos(self):
        for record in self:
            record.total_mantenimientos = len(record.mantenimiento_ids)

    @api.constrains('estado_mecanico', 'estado_exterior', 'estado_interior',
                    'nivel_combustible', 'documentacion')
    def _check_puntajes_rango(self):
        for record in self:
            campos = [
                ('Estado Mecánico', record.estado_mecanico),
                ('Estado Exterior', record.estado_exterior),
                ('Estado Interior', record.estado_interior),
                ('Nivel Combustible', record.nivel_combustible),
                ('Documentación', record.documentacion),
            ]
            for nombre, valor in campos:
                if valor < 0 or valor > 10:
                    raise ValidationError(f'El puntaje de {nombre} debe estar entre 0 y 10.')

    @api.constrains('kilometraje')
    def _check_kilometraje(self):
        for record in self:
            if record.kilometraje < 0:
                raise ValidationError('El kilometraje no puede ser negativo.')

    @api.onchange('vehiculo_id')
    def _onchange_vehiculo_id(self):
        if self.vehiculo_id:
            # Aquí podrías buscar el último kilometraje registrado
            return {'warning': {
                'title': 'Verificación',
                'message': 'Por favor verifique que el kilometraje ingresado sea mayor al último registrado.'
            }}

    def action_calificar(self):
        for record in self:
            record.state = 'calificado'

    def action_revisar(self):
        for record in self:
            record.state = 'revisado'

    def action_aprobar(self):
        for record in self:
            record.state = 'aprobado'


class VehiculoMantenimiento(models.Model):
    _name = 'ou.vehiculo.mantenimiento'
    _description = 'Registro de Mantenimiento de Vehículo'

    calificacion_id = fields.Many2one(
        'ou.calificacion.vehiculo',
        string='Calificación',
        required=True,
        ondelete='cascade'
    )
    fecha_mantenimiento = fields.Date(string='Fecha de Mantenimiento', required=True, default=fields.Date.today)
    tipo_mantenimiento = fields.Selection([
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
        ('predictivo', 'Predictivo'),
    ], string='Tipo', required=True)
    descripcion = fields.Text(string='Descripción del Trabajo', required=True)
    costo = fields.Monetary(string='Costo', currency_field='currency_id', default=0.0)
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id
    )
    tecnico_id = fields.Many2one('res.users', string='Técnico Responsable')
    proximo_mantenimiento = fields.Date(string='Próximo Mantenimiento Programado')
    estado = fields.Selection([
        ('programado', 'Programado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='programado')

    @api.constrains('costo')
    def _check_costo_positivo(self):
        for record in self:
            if record.costo < 0:
                raise ValidationError('El costo del mantenimiento no puede ser negativo.')

    @api.constrains('fecha_mantenimiento', 'proximo_mantenimiento')
    def _check_fechas_mantenimiento(self):
        for record in self:
            if record.proximo_mantenimiento and record.proximo_mantenimiento <= record.fecha_mantenimiento:
<<<<<<< HEAD
                raise ValidationError('La fecha del próximo mantenimiento debe ser posterior a la fecha actual del mantenimiento.')
=======
                raise ValidationError('La fecha del próximo mantenimiento debe ser posterior a la fecha actual del mantenimiento.')
>>>>>>> c1b48e8873a20a5a1324a750d1a52238c1f0fcc6
